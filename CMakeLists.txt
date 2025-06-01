cmake_minimum_required(VERSION 3.10)

# Project name
project(Castle)



# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Automatically find all .cpp and .h files in the current directory
file(GLOB SOURCES "./src/*.cpp")
file(GLOB HEADERS "./src/*.h")

# Find Python
find_package(Python3 REQUIRED COMPONENTS Interpreter Development)

# Add pybind11
add_subdirectory(extern/pybind11)

# Create the executable
add_executable(testCastle ${SOURCES})

target_link_libraries(testCastle 
    PRIVATE 
        pybind11::headers
        Python3::Python
)
target_include_directories(testCastle PRIVATE extern/pybind11/include)

