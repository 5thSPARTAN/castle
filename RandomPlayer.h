#ifndef RANDOMPLAYER_H
#define RANDOMPLAYER_H

#include "Observation.h"
#include <random>

class RandomPlayer{
private:

public:
    RandomPlayer();
    ~RandomPlayer();
    int pickAction(Observation);
};

#endif