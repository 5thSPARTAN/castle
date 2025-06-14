#include "GameEnv.h"
#include "Player.h"
#include "RandomPlayer.h"
#include <iostream>

void printStepOutput( tuple<deque<Observation>, deque<float>, bool> input);
void printFeatures(Observation obs);
void printActions(Observation obs);

int main(){
    
    GameEnv testGame(4,5,7);
    
    tuple<deque<Observation>, deque<float>, bool> output;
    RandomPlayer randPlayer;
    deque<int> actionList = {0,0,0,0};

    output = testGame.step(actionList);
    //printStepOutput(output);
    while(!get<2>(output)){
        actionList = {};
        for(Observation obs: get<0>(output)){
            actionList.push_back(randPlayer.pickAction(obs));
        }
//        cout << "actions: ";
//        for(int x : actionList){
//            cout << x << ", ";
//        }
//        cout << endl;
        output = testGame.step(actionList);
        //printStepOutput(output);
    }
    
//    cout << "Done" << endl;

    

}

void printStepOutput( tuple<deque<Observation>,deque<float>, bool> input){
    printFeatures(get<0>(input)[0]);
    for( int i = 0; i < get<0>(input).size(); i++){
        cout << "Player " << i << endl;
        printActions(get<0>(input)[i]);
        cout << endl << endl;
    }
}
void printFeatures(Observation obs){
    cout << "PLAYER NUMBER         : " << obs.features[0] << endl; 
    cout << "NUMBER OF PLAYERS LEFT: " << obs.features[1] << endl; 
    cout << "MAX HEALTH            : " << obs.features[2] << endl; 
    cout << "PLAYER 0 HEALTH       : " << obs.features[3] << endl; 
    cout << "PLAYER 0 CARDS IN DECK: " << obs.features[4] << endl; 
    cout << "PLAYER 0 CARDS IN JAIL: " << obs.features[5] << endl; 
    cout << "PLAYER 0 CARDS IN HAND: " << obs.features[6] << endl; 
    cout << "PLAYER 1 HEALTH       : " << obs.features[7] << endl; 
    cout << "PLAYER 1 CARDS IN DECK: " << obs.features[8] << endl; 
    cout << "PLAYER 1 CARDS IN JAIL: " << obs.features[9] << endl; 
    cout << "PLAYER 1 CARDS IN HAND: " << obs.features[10] << endl; 
    cout << "PLAYER 2 HEALTH       : " << obs.features[11] << endl; 
    cout << "PLAYER 2 CARDS IN DECK: " << obs.features[12] << endl; 
    cout << "PLAYER 2 CARDS IN JAIL: " << obs.features[13] << endl; 
    cout << "PLAYER 2 CARDS IN HAND: " << obs.features[14] << endl; 
    cout << "PLAYER 3 HEALTH       : " << obs.features[15] << endl; 
    cout << "PLAYER 3 CARDS IN DECK: " << obs.features[16] << endl; 
    cout << "PLAYER 3 CARDS IN JAIL: " << obs.features[17] << endl; 
    cout << "PLAYER 3 CARDS IN HAND: " << obs.features[18] << endl; 
    cout << "WAR                   : " << obs.features[19] << endl; 
    cout << "INFILTRATING          : " << obs.features[20] << endl; 
    cout << "INFILTRATED PLAYER    : " << obs.features[21] << endl; 
    cout << "CARD PULLED LOCATION  : " << obs.features[22] << endl; 
}
void printActions(Observation obs){
    if(obs.actionMask[0]){ cout << "DO NOTHING (dead/war/infiltrating)" << endl;}
    if(obs.actionMask[1]){ cout << "(2) PLAYER SWAPS NOTHING" << endl;}
    if(obs.actionMask[2]){ cout << "(2) PLAYER SWAPS 2" << endl;}
    if(obs.actionMask[3]){ cout << "(2) PLAYER SWAPS 3" << endl;}
    if(obs.actionMask[4]){ cout << "(2) PLAYER SWAPS 4" << endl;}
    if(obs.actionMask[5]){ cout << "(2) PLAYER SWAPS 5" << endl;}
    if(obs.actionMask[6]){ cout << "(2) PLAYER SWAPS 6" << endl;}
    if(obs.actionMask[7]){ cout << "(2) PLAYER SWAPS 7" << endl;}
    if(obs.actionMask[8]){ cout << "(2) PLAYER SWAPS 8" << endl;}
    if(obs.actionMask[9]){ cout << "(2) PLAYER SWAPS 9" << endl;}
    if(obs.actionMask[10]){cout << "(2) PLAYER SWAPS 10" << endl;}
    if(obs.actionMask[11]){cout << "(2) PLAYER SWAPS 11" << endl;}
    if(obs.actionMask[12]){cout << "(2) PLAYER SWAPS 12" << endl;}
    if(obs.actionMask[13]){cout << "(2) PLAYER SWAPS 13" << endl;}
    if(obs.actionMask[14]){cout << "PLAYER PLAYS 3 " << endl;}
    if(obs.actionMask[15]){cout << "PLAYER PLAYS 4" << endl;}
    if(obs.actionMask[16]){cout << "PLAYER PLAYS 5" << endl;}
    if(obs.actionMask[17]){cout << "PLAYER PLAYS 6" << endl;}
    if(obs.actionMask[18]){cout << "PLAYER PLAYS 7" << endl;}
    if(obs.actionMask[19]){cout << "PLAYER PLAYS 8" << endl;}
    if(obs.actionMask[20]){cout << "PLAYER PLAYS 9" << endl;}
    if(obs.actionMask[21]){cout << "PLAYER PLAYS 10" << endl;}
    if(obs.actionMask[22]){cout << "PLAYER PLAYS 11" << endl;}
    if(obs.actionMask[23]){cout << "PLAYER PLAYS 12" << endl;}
    if(obs.actionMask[24]){cout << "PLAYER PLAYS 13" << endl;}
    if(obs.actionMask[25]){cout << "PLAYER PLAYS 2 ON PLAYER 0" << endl;}
    if(obs.actionMask[26]){cout << "PLAYER PLAYS 2 ON PLAYER 1" << endl;}
    if(obs.actionMask[27]){cout << "PLAYER PLAYS 2 ON PLAYER 2" << endl;}
    if(obs.actionMask[28]){cout << "PLAYER PLAYS 2 ON PLAYER 3" << endl;}
}