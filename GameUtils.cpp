#include "GameUtils.h"

// input a list of player numbers and their cards
// output a list of players who won and their cards
deque<deque<int>> findWinners(deque<deque<int>> input){
    int winnerCard = input[0][1];
    bool assassin3 = false;
    bool assassin4 = false;


    // find highest card
    for( deque<int> i : input){
        if(i[1] > winnerCard){
            winnerCard = i[1];
        }
        if(i[1] == 3){
            assassin3 = true;
        }
        if(i[1] == 4){
            assassin4 = true;
        }
    }
    // check assasin
    if( assassin4 && winnerCard >= 11){
        winnerCard = 4;
    }
    else if ( assassin3 && winnerCard >=11){
        winnerCard = 3;
    }

    // populate winners
    deque<deque<int>> winners;
    for( deque<int> i : input){
        if(i[1] == winnerCard){
            winners.push_back({i});
        }
    }
    return winners;
}