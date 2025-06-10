#include "RandomPlayer.h"
#include <deque>


int RandomPlayer::pickAction(Observation obs){
    deque<int> trueIndices;
    for( int i = 0; i < obs.actionMask.size(); i++){
        if(obs.actionMask[i]){
            trueIndices.push_back(i);
        }
    }
    
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> dist(0, static_cast<int>(trueIndices.size() -1));

    return trueIndices[dist(gen)];
}