#include "GameEnv.h"

GameEnv::GameEnv(int p, int s, int m){
    players = p;
    startingHealth = s;
    maxHealth = m;
    game_ = Game(players, startingHealth, maxHealth);
}

GameEnv::~GameEnv(){}

void GameEnv::reset(){
    game_ = Game(players, startingHealth, maxHealth);
}

tuple<Observation, float, bool> GameEnv::step(int action){
    
}