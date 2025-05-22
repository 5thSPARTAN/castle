cmake_minimum_required(VERSION 3.10)

# Project name
project(Castle)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Automatically find all .cpp and .h files in the current directory
file(GLOB SOURCES "*.cpp")
file(GLOB HEADERS "*.h")

# Create the executable
add_executable(testCastle ${SOURCES})
