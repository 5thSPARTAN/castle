#include "Observation.h"
#include "GameEnv.h"
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>


namespace py = pybind11;

PYBIND11_MODULE(game_env, m) {
    py::class_<GameEnv>(m, "GameEnv")
        .def(py::init<int,int,int>())
        .def("reset", &GameEnv::reset, "A function which resets the game")
        .def("step", &GameEnv::step, py::arg("actions"));
    py::class_<Observation>(m, "Observation")
        .def(py::init<>())
        .def_readwrite("features", &Observation::features)
        .def_readwrite("actionMask", &Observation::actionMask);
}