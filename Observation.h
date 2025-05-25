#ifndef OBSERVATION_H
#define OBSERVATION_H

#include <vector>
using namespace std;

struct Observation{
    vector<float> features;
    vector<bool> actionMask;
};

#endif