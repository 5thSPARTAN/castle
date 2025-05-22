#ifndef PLAYER_H
#define PLAYER_H

#include <vector>
#include <random> // for random
#include <algorithm> // for shuffle
using namespace std;

// for testing
#include <iostream>


class Player{
private:
    vector<int> deck;
    vector<int> jail;
    vector<int> hand;
    int playerNumber;
    int health;

public:
    Player(int playerNumber, int health);
    void printPlayer();

};

#endif