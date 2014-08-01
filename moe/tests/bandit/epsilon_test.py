# -*- coding: utf-8 -*-
"""Test epsilon bandit implementation (functions common to epsilon bandit).

Test functions in :class:`moe.bandit.epsilon.Epsilon`

"""
import testify as T

from moe.bandit.epsilon import Epsilon
from moe.tests.bandit.epsilon_test_case import EpsilonTestCase


class EpsilonTest(EpsilonTestCase):

    """Verify that different sample_arms return correct results."""

    def test_two_new_arms(self):
        """Check that the two-new-arms case always returns both arms as winning arms. This tests num_winning_arms == num_arms > 1."""
        T.assert_sets_equal(Epsilon.get_winning_arm_names(self.two_new_arms_test_case.arms_sampled), frozenset(["arm1", "arm2"]))

    def test_three_arms_two_winners(self):
        """Check that the three-arms cases with two winners return the expected winning arms. This tests num_arms > num_winning_arms > 1."""
        T.assert_sets_equal(Epsilon.get_winning_arm_names(self.three_arms_two_winners_test_case.arms_sampled), frozenset(["arm1", "arm2"]))


if __name__ == "__main__":
    T.run()