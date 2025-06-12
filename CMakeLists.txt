cmake_minimum_required(VERSION 3.10)

# Project name
project(Castle)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Add pybind11
add_subdirectory(extern/pybind11)

# Automatically find all .cpp and .h files in the current directory
file(GLOB SOURCES "./src/*.cpp")
file(GLOB HEADERS "./src/*.h")

# create a python module
pybind11_add_module(game_env ${SOURCES})

add_executable(testCastle ${SOURCES})

target_link_libraries(testCastle PRIVATE pybind11::module)