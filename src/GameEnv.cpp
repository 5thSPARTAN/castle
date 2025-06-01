#include <pybind11>
#include "GameEnv.h"

GameEnv::GameEnv(int p, int s, int m){
    players = p;
    startingHealth = s;
    maxHealth = m;
    game_ = Game(players, startingHealth, maxHealth);
}

GameEnv::~GameEnv(){}

deque<Observation> GameEnv::reset(){
    game_ = Game(players, startingHealth, maxHealth);
    deque<Observation> obs;
    obs.push_back(game_.toObservation(0));
    obs.push_back(game_.toObservation(1));
    obs.push_back(game_.toObservation(2));
    obs.push_back(game_.toObservation(3));
    return obs;
}

tuple<deque<Observation>, deque<float>, bool> GameEnv::step(deque<int> action){
    game_.applyAction(action);
    deque<Observation> obs;
    obs.push_back(game_.toObservation(0));
    obs.push_back(game_.toObservation(1));
    obs.push_back(game_.toObservation(2));
    obs.push_back(game_.toObservation(3));

    deque<float> rewards;
    rewards.push_back(static_cast<float>(game_.isWin(0)));
    rewards.push_back(static_cast<float>(game_.isWin(1)));
    rewards.push_back(static_cast<float>(game_.isWin(2)));
    rewards.push_back(static_cast<float>(game_.isWin(3)));

    return {obs, rewards, game_.isOver()};
    
}