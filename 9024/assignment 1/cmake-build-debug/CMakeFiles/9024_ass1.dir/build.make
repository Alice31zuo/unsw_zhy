# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.14

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


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
CMAKE_COMMAND = /Applications/CLion.app/Contents/bin/cmake/mac/bin/cmake

# The command to remove a file.
RM = /Applications/CLion.app/Contents/bin/cmake/mac/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /Users/alice/CLionProjects/9024_ass1

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/alice/CLionProjects/9024_ass1/cmake-build-debug

# Include any dependencies generated for this target.
include CMakeFiles/9024_ass1.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/9024_ass1.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/9024_ass1.dir/flags.make

CMakeFiles/9024_ass1.dir/boardADT.c.o: CMakeFiles/9024_ass1.dir/flags.make
CMakeFiles/9024_ass1.dir/boardADT.c.o: ../boardADT.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/alice/CLionProjects/9024_ass1/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building C object CMakeFiles/9024_ass1.dir/boardADT.c.o"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/9024_ass1.dir/boardADT.c.o   -c /Users/alice/CLionProjects/9024_ass1/boardADT.c

CMakeFiles/9024_ass1.dir/boardADT.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/9024_ass1.dir/boardADT.c.i"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /Users/alice/CLionProjects/9024_ass1/boardADT.c > CMakeFiles/9024_ass1.dir/boardADT.c.i

CMakeFiles/9024_ass1.dir/boardADT.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/9024_ass1.dir/boardADT.c.s"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /Users/alice/CLionProjects/9024_ass1/boardADT.c -o CMakeFiles/9024_ass1.dir/boardADT.c.s

CMakeFiles/9024_ass1.dir/puzzle.c.o: CMakeFiles/9024_ass1.dir/flags.make
CMakeFiles/9024_ass1.dir/puzzle.c.o: ../puzzle.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/alice/CLionProjects/9024_ass1/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building C object CMakeFiles/9024_ass1.dir/puzzle.c.o"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/9024_ass1.dir/puzzle.c.o   -c /Users/alice/CLionProjects/9024_ass1/puzzle.c

CMakeFiles/9024_ass1.dir/puzzle.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/9024_ass1.dir/puzzle.c.i"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /Users/alice/CLionProjects/9024_ass1/puzzle.c > CMakeFiles/9024_ass1.dir/puzzle.c.i

CMakeFiles/9024_ass1.dir/puzzle.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/9024_ass1.dir/puzzle.c.s"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /Users/alice/CLionProjects/9024_ass1/puzzle.c -o CMakeFiles/9024_ass1.dir/puzzle.c.s

# Object files for target 9024_ass1
9024_ass1_OBJECTS = \
"CMakeFiles/9024_ass1.dir/boardADT.c.o" \
"CMakeFiles/9024_ass1.dir/puzzle.c.o"

# External object files for target 9024_ass1
9024_ass1_EXTERNAL_OBJECTS =

9024_ass1: CMakeFiles/9024_ass1.dir/boardADT.c.o
9024_ass1: CMakeFiles/9024_ass1.dir/puzzle.c.o
9024_ass1: CMakeFiles/9024_ass1.dir/build.make
9024_ass1: CMakeFiles/9024_ass1.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/alice/CLionProjects/9024_ass1/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Linking C executable 9024_ass1"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/9024_ass1.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/9024_ass1.dir/build: 9024_ass1

.PHONY : CMakeFiles/9024_ass1.dir/build

CMakeFiles/9024_ass1.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/9024_ass1.dir/cmake_clean.cmake
.PHONY : CMakeFiles/9024_ass1.dir/clean

CMakeFiles/9024_ass1.dir/depend:
	cd /Users/alice/CLionProjects/9024_ass1/cmake-build-debug && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/alice/CLionProjects/9024_ass1 /Users/alice/CLionProjects/9024_ass1 /Users/alice/CLionProjects/9024_ass1/cmake-build-debug /Users/alice/CLionProjects/9024_ass1/cmake-build-debug /Users/alice/CLionProjects/9024_ass1/cmake-build-debug/CMakeFiles/9024_ass1.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/9024_ass1.dir/depend

