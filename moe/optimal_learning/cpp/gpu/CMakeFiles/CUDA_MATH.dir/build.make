# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 2.8

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list

# Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/local/bin/cmake

# The command to remove a file.
RM = /usr/local/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The program to use to edit the cache.
CMAKE_EDIT_COMMAND = /usr/local/bin/ccmake

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /fs/home/jw865/Documents/gpu/moe/optimal_learning/cpp/gpu

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /fs/home/jw865/Documents/gpu/moe/optimal_learning/cpp/gpu

# Include any dependencies generated for this target.
include CMakeFiles/CUDA_MATH.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/CUDA_MATH.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/CUDA_MATH.dir/flags.make

CMakeFiles/CUDA_MATH.dir/./CUDA_MATH_generated_gpp_cuda_math.cu.o: CMakeFiles/CUDA_MATH.dir/CUDA_MATH_generated_gpp_cuda_math.cu.o.depend
CMakeFiles/CUDA_MATH.dir/./CUDA_MATH_generated_gpp_cuda_math.cu.o: CMakeFiles/CUDA_MATH.dir/CUDA_MATH_generated_gpp_cuda_math.cu.o.cmake
CMakeFiles/CUDA_MATH.dir/./CUDA_MATH_generated_gpp_cuda_math.cu.o: gpp_cuda_math.cu
	$(CMAKE_COMMAND) -E cmake_progress_report /fs/home/jw865/Documents/gpu/moe/optimal_learning/cpp/gpu/CMakeFiles $(CMAKE_PROGRESS_1)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold "Building NVCC (Device) object CMakeFiles/CUDA_MATH.dir//./CUDA_MATH_generated_gpp_cuda_math.cu.o"
	cd /fs/home/jw865/Documents/gpu/moe/optimal_learning/cpp/gpu/CMakeFiles/CUDA_MATH.dir && /usr/local/bin/cmake -E make_directory /fs/home/jw865/Documents/gpu/moe/optimal_learning/cpp/gpu/CMakeFiles/CUDA_MATH.dir//.
	cd /fs/home/jw865/Documents/gpu/moe/optimal_learning/cpp/gpu/CMakeFiles/CUDA_MATH.dir && /usr/local/bin/cmake -D verbose:BOOL=$(VERBOSE) -D build_configuration:STRING= -D generated_file:STRING=/fs/home/jw865/Documents/gpu/moe/optimal_learning/cpp/gpu/CMakeFiles/CUDA_MATH.dir//./CUDA_MATH_generated_gpp_cuda_math.cu.o -D generated_cubin_file:STRING=/fs/home/jw865/Documents/gpu/moe/optimal_learning/cpp/gpu/CMakeFiles/CUDA_MATH.dir//./CUDA_MATH_generated_gpp_cuda_math.cu.o.cubin.txt -P /fs/home/jw865/Documents/gpu/moe/optimal_learning/cpp/gpu/CMakeFiles/CUDA_MATH.dir//CUDA_MATH_generated_gpp_cuda_math.cu.o.cmake

# Object files for target CUDA_MATH
CUDA_MATH_OBJECTS =

# External object files for target CUDA_MATH
CUDA_MATH_EXTERNAL_OBJECTS = \
"/fs/home/jw865/Documents/gpu/moe/optimal_learning/cpp/gpu/CMakeFiles/CUDA_MATH.dir/./CUDA_MATH_generated_gpp_cuda_math.cu.o"

libCUDA_MATH.so: CMakeFiles/CUDA_MATH.dir/./CUDA_MATH_generated_gpp_cuda_math.cu.o
libCUDA_MATH.so: CMakeFiles/CUDA_MATH.dir/build.make
libCUDA_MATH.so: /opt/nvidia/cuda/lib64/libcudart.so
libCUDA_MATH.so: CMakeFiles/CUDA_MATH.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --red --bold "Linking CXX shared library libCUDA_MATH.so"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/CUDA_MATH.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/CUDA_MATH.dir/build: libCUDA_MATH.so
.PHONY : CMakeFiles/CUDA_MATH.dir/build

CMakeFiles/CUDA_MATH.dir/requires:
.PHONY : CMakeFiles/CUDA_MATH.dir/requires

CMakeFiles/CUDA_MATH.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/CUDA_MATH.dir/cmake_clean.cmake
.PHONY : CMakeFiles/CUDA_MATH.dir/clean

CMakeFiles/CUDA_MATH.dir/depend: CMakeFiles/CUDA_MATH.dir/./CUDA_MATH_generated_gpp_cuda_math.cu.o
	cd /fs/home/jw865/Documents/gpu/moe/optimal_learning/cpp/gpu && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /fs/home/jw865/Documents/gpu/moe/optimal_learning/cpp/gpu /fs/home/jw865/Documents/gpu/moe/optimal_learning/cpp/gpu /fs/home/jw865/Documents/gpu/moe/optimal_learning/cpp/gpu /fs/home/jw865/Documents/gpu/moe/optimal_learning/cpp/gpu /fs/home/jw865/Documents/gpu/moe/optimal_learning/cpp/gpu/CMakeFiles/CUDA_MATH.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/CUDA_MATH.dir/depend
