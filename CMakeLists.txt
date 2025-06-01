cmake_minimum_required(VERSION 3.10)

# Project name
project(Castle)

# Add pybind11
add_subdirectory(extern/pybind11)

# Define your binding module
pybind11_add_module(gameenv src/GameEnv.cpp)


# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Automatically find all .cpp and .h files in the current directory
file(GLOB SOURCES "./src/*.cpp")
file(GLOB HEADERS "./src/*.h")

# Create the executable
add_executable(testCastle ${SOURCES})
