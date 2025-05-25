#include "Game.h"
#include "Player.h"
#include <iostream>

int main(){
    
    Game testGame(2, 5,7);
    testGame.printGame();
    
    deque<deque<int>> battleInput;
    battleInput.push_back({0,0});
    battleInput.push_back({1,0});

    cout << "Player 0 card: ";
    cin >> battleInput[0][1];

    while(battleInput[0][1] == 2){
        int chosenPlayer;
        cout << "Which player do you want to infiltrate: ";
        cin >> chosenPlayer;
        deque<int> dataExtracted = testGame.infiltrate(0, chosenPlayer);
        cout << "You have pulled a " << dataExtracted[0] << " from Player " << chosenPlayer << "." << endl;
        switch(dataExtracted[1]){
            case 0:
                cout << "It is currently in your deck." << endl;
                break;
            case 1:
                cout << "It is currently in your jail." << endl;
                break;
            case 2:
                cout << "It is currently in your hand." << endl;
                break;
        }
        int swapDecision;
        cout << "Would you like to swap? 0 for no swap, 1 for swap: ";
        cin >> swapDecision;
        if(swapDecision == 1){
            testGame.infiltrateSwap(0, chosenPlayer, dataExtracted[0], dataExtracted[1])
        }
        testGame.printGame();
        cout << "Please play new card Player 0: ";
        cin >> battleInput[0][1];
    }

    cout << "Player 1 card: ";
    cin >> battleInput[1][1];

    while(battleInput[1][1] == 2){
        int chosenPlayer;
        cout << "Which player do you want to infiltrate: ";
        cin >> chosenPlayer;
        deque<int> dataExtracted = testGame.infiltrate(1, chosenPlayer);
        cout << "You have pulled a " << dataExtracted[0] << " from Player " << chosenPlayer << "." << endl;
        switch(dataExtracted[1]){
            case 0:
                cout << "It is currently in your deck." << endl;
                break;
            case 1:
                cout << "It is currently in your jail." << endl;
                break;
            case 2:
                cout << "It is currently in your hand." << endl;
                break;
        }
        int swapDecision;
        cout << "Would you like to swap? 0 for no swap, 1 for swap: ";
        cin >> swapDecision;
        if(swapDecision == 1){
            testGame.infiltrateSwap(1, chosenPlayer, dataExtracted[0], dataExtracted[1]);
        }
        testGame.printGame();
        cout << "Please play new card Player 1: ";
        cin >> battleInput[1][1];
    }

//    cout << battleInput.size() << endl;
//    for( deque<int> i : battleInput){
//        for( int j : i){
//            cout << j << ", ";
//        }
//        cout << endl;
//    }
//    cout << endl;

    deque<deque<int>> battleOutput = testGame.battle(battleInput);
    deque<deque<int>> cardsPlayed;
    while(battleInput.size() != 0){
        cardsPlayed.push_back(battleInput.back());
        battleInput.pop_back();
    }
    while(battleOutput.size() > 1){
        cout << "war has started" << endl;
        testGame.printGame();
        for(deque<int> i : battleOutput){
            int newCard;
            cout << "Player " << i[0] << "new card: ";
            cin >> newCard;
            battleInput.push_back({i[0],newCard});
        }
        battleOutput = testGame.battle(battleInput);
        while(battleInput.size() != 0){
            cardsPlayed.push_back(battleInput.back());
            battleInput.pop_back();
        }
    }

//    cout << cardsPlayed.size() << endl;
//    for( deque<int> i : cardsPlayed){
//        for( int j : i){
//            cout << j << ", ";
//        }
//        cout << endl;
//    }
//    cout << endl;

    testGame.playerWins(battleOutput[0][0], cardsPlayed);
    cout << "Player " << battleOutput[0][0] << " won with " << battleOutput[0][1] << endl << endl;
    testGame.printGame();
    
    /*
    cout << endl << endl;

    Player testPlayer(2,5,7);
    testPlayer.printPlayer();
    cout << endl << endl;

    testPlayer.damage();
    testPlayer.printPlayer();
    cout << endl << endl;

    testPlayer.heal();
    testPlayer.printPlayer();
    cout << endl << endl;

    testPlayer.discardHand();
    testPlayer.printPlayer();
    cout << endl << endl;
    */

}