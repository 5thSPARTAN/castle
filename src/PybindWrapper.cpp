#include <pybind11/pybind11.h>

#include "GameEnv.h"

namespace py = pybind11;

PYBIND11_MODULE(game_env, m) {
    py::class_<GameEnv>(m, "GameEnv")
    .def(py::init<int,int,int>())
    .def("reset", &GameEnv::reset, "A function which resets the game")
    .def("step", &GameEnv::step, py::arg("actions"));
}