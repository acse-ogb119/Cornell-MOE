# -*- coding: utf-8 -*-
"""Implementation (Python) of GaussianProcessInterface.
This file contains a class to manipulate a Gaussian Process through numpy/scipy.
See :mod:`moe.optimal_learning.python.interfaces.gaussian_process_interface` for more details.
"""
import copy

import numpy
import emcee

import moe.build.GPP as C_GP
from moe.optimal_learning.python.cpp_wrappers import cpp_utils
from moe.optimal_learning.python.cpp_wrappers.covariance import SquareExponential
from moe.optimal_learning.python.cpp_wrappers.gaussian_process import GaussianProcess
from moe.optimal_learning.python.cpp_wrappers.knowledge_gradient_mcmc import GaussianProcessMCMC

class AdditiveKernelMCMC(object):

    r"""Class for computing log likelihood-like measures of additive kernel model fit.
    """

    def __init__(self, historical_data, derivatives, prior, chain_length, burnin_steps, n_hypers,
                 log_likelihood_type=C_GP.LogLikelihoodTypes.log_marginal_likelihood, noisy = True, rng = None):
        """Construct a LogLikelihood object that knows how to call C++ for evaluation of member functions.
        :param covariance_function: covariance object encoding assumptions about the GP's behavior on our data
        :type covariance_function: :class:`moe.optimal_learning.python.interfaces.covariance_interface.CovarianceInterface` subclass
          (e.g., from :mod:`moe.optimal_learning.python.cpp_wrappers.covariance`).
        :param historical_data: object specifying the already-sampled points, the objective value at those points, and the noise variance associated with each observation
        :type historical_data: :class:`moe.optimal_learning.python.data_containers.HistoricalData` object
        """
        self._historical_data = copy.deepcopy(historical_data)

        self._derivatives = copy.deepcopy(derivatives)
        self._num_derivatives = len(cpp_utils.cppify(self._derivatives))

        self.objective_type = log_likelihood_type

        self.prior = prior
        self.chain_length = chain_length
        self.burned = False
        self.burnin_steps = burnin_steps
        self._models = []
        self.noisy = noisy

        if rng is None:
            self.rng = numpy.random.RandomState(numpy.random.randint(0, 10000))
        else:
            self.rng = rng
        self.n_hypers = n_hypers
        self.n_chains = max(n_hypers, 2*(2*self._historical_data.dim+1+self._num_derivatives))

    @property
    def dim(self):
        """Return the number of spatial dimensions."""
        return self._historical_data.dim

    @property
    def _num_sampled(self):
        """Return the number of sampled points."""
        return self._historical_data.num_sampled

    @property
    def _points_sampled(self):
        """Return the coordinates of the already-sampled points; see :class:`moe.optimal_learning.python.data_containers.HistoricalData`."""
        return self._historical_data.points_sampled

    @property
    def _points_sampled_value(self):
        """Return the function values measured at each of points_sampled; see :class:`moe.optimal_learning.python.data_containers.HistoricalData`."""
        return self._historical_data.points_sampled_value

    @property
    def _points_sampled_noise_variance(self):
        """Return the noise variance associated with points_sampled_value; see :class:`moe.optimal_learning.python.data_containers.HistoricalData`."""
        return self._historical_data.points_sampled_noise_variance

    @property
    def models(self):
        return self._models

    def get_historical_data_copy(self):
        """Return the data (points, function values, noise) specifying the prior of the Gaussian Process.
        :return: object specifying the already-sampled points, the objective value at those points, and the noise variance associated with each observation
        :rtype: data_containers.HistoricalData
        """
        return copy.deepcopy(self._historical_data)

    def train(self, do_optimize=True, **kwargs):
        """
        Performs MCMC sampling to sample hyperparameter configurations from the
        likelihood and trains for each sample a GP on X and y

        Parameters
        ----------
        X: np.ndarray (N, D)
            Input data points. The dimensionality of X is (N, D),
            with N as the number of points and D is the number of features.
        y: np.ndarray (N,)
            The corresponding target values.
        do_optimize: boolean
            If set to true we perform MCMC sampling otherwise we just use the
            hyperparameter specified in the kernel.
        """

        if do_optimize:
            # We have one walker for each hyperparameter configuration
            sampler = emcee.EnsembleSampler(self.n_chains,
                                            2*self.dim + self._num_derivatives + 1,
                                            self.compute_log_likelihood)

            # Do a burn-in in the first iteration
            if not self.burned:
                # Initialize the walkers by sampling from the prior
                if self.prior is None:
                    self.p0 = numpy.random.rand(self.n_chains, 2*self.dim + self._num_derivatives + 1)
                else:
                    self.p0 = self.prior.sample_from_prior(self.n_chains)
                # Run MCMC sampling
                self.p0, _, _ = sampler.run_mcmc(self.p0,
                                                 self.burnin_steps,
                                                 rstate0=self.rng)

                self.burned = True

            # Start sampling
            pos, _, _ = sampler.run_mcmc(self.p0, self.chain_length, rstate0=self.rng)

            # Save the current position, it will be the start point in
            # the next iteration
            self.p0 = pos

            # Take the last samples from each walker
            self.hypers = sampler.chain[numpy.random.choice(self.n_chains, self.n_hypers), -1]

        self.is_trained = True
        self._models = []
        hypers_list = []
        noises_list = []
        for sample in self.hypers:
            if numpy.any((-20 > sample) + (sample > 20)):
                continue
            sample = numpy.exp(sample)
            # Instantiate a GP for each hyperparameter configuration
            cov_hyps = sample[:(2*self.dim)]
            hypers_list.append(cov_hyps)
            se = SquareExponential(cov_hyps)
            if self.noisy:
                noise = sample[(2*self.dim):]
            else:
                noise = numpy.array([1.e-8]*(1+len(self._derivatives)))
            noises_list.append(noise)
            model = GaussianProcess(se, noise, self._historical_data, self._derivatives)
            self._models.append(model)

        self._gaussian_process_mcmc = GaussianProcessMCMC(numpy.array(hypers_list), numpy.array(noises_list),
                                                          self._historical_data, self._derivatives)

    def compute_log_likelihood(self, hyps):
        r"""Compute the objective_type measure at the specified hyperparameters.

        :return: value of log_likelihood evaluated at hyperparameters (``LL(y | X, \theta)``)
        :rtype: float64

        """
        # Bound the hyperparameter space to keep things sane. Note all
        # hyperparameters live on a log scale
        if numpy.any((-20 > hyps) + (hyps > 20)):
            return -numpy.inf
        hyps = numpy.exp(hyps)
        cov_hyps = hyps[:(2*self.dim)]
        noise = hyps[(2*self.dim):]
        if not self.noisy:
            noise = numpy.array([1.e-8]*(1+len(self._derivatives)))
        try:
            if self.prior is not None:
                posterior = self.prior.lnprob(numpy.log(hyps))
                return posterior + C_GP.compute_log_likelihood(
                        cpp_utils.cppify(self._points_sampled),
                        cpp_utils.cppify(self._points_sampled_value),
                        self.dim,
                        self._num_sampled,
                        self.objective_type,
                        cpp_utils.cppify_hyperparameters(cov_hyps),
                        cpp_utils.cppify(self._derivatives), self._num_derivatives,
                        cpp_utils.cppify(noise),
                )
            else:
                return C_GP.compute_log_likelihood(
                        cpp_utils.cppify(self._points_sampled),
                        cpp_utils.cppify(self._points_sampled_value),
                        self.dim,
                        self._num_sampled,
                        self.objective_type,
                        cpp_utils.cppify_hyperparameters(cov_hyps),
                        cpp_utils.cppify(self._derivatives), self._num_derivatives,
                        cpp_utils.cppify(noise),
                )
        except:
            return -numpy.inf

    def add_sampled_points(self, sampled_points):
        r"""Add sampled point(s) (point, value, noise) to the GP's prior data.
        Also forces recomputation of all derived quantities for GP to remain consistent.
        :param sampled_points: :class:`moe.optimal_learning.python.SamplePoint` objects to load
          into the GP (containing point, function value, and noise variance)
        :type sampled_points: list of :class:`~moe.optimal_learning.python.SamplePoint` objects (or SamplePoint-like iterables)
        """
        # TODO(GH-159): When C++ can pass back numpy arrays, we can stop keeping a duplicate in self._historical_data.
        self._historical_data.append_sample_points(sampled_points)
        if len(self.models) > 0:
            for model in self._models:
                model.add_sampled_points(sampled_points)