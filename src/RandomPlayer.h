#ifndef RANDOMPLAYER_H
#define RANDOMPLAYER_H

#include "Observation.h"
#include <random>

using namespace std;

class RandomPlayer{
private:

public:
    RandomPlayer() = default;
    ~RandomPlayer() = default;
    static int pickAction(Observation);
};

#endif