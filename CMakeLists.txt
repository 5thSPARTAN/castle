cmake_minimum_required(VERSION 3.10)

# Project name
project(Castle)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)
set(CMAKE_BUILD_TYPE RelWithDebInfo)

# Find Python interpreter, libraries, and headers
find_package(Python3 REQUIRED COMPONENTS Interpreter Development)

# Add pybind11
add_subdirectory(extern/pybind11)

# Automatically find all .cpp and .h files in the current directory
file(GLOB SOURCES "./src/*.cpp")
file(GLOB HEADERS "./src/*.h")

# create a python module
pybind11_add_module(game_env ${SOURCES})
target_compile_options(game_env PRIVATE -g)

add_executable(testCastle ${SOURCES})

target_include_directories(testCastle PRIVATE ${Python3_INCLUDE_DIRS})
target_link_libraries(testCastle PRIVATE ${Python3_LIBRARIES} pybind11::module)