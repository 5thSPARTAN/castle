#include "Game.h"
#include "Player.h"
#include <iostream>

int main(){
    Game testGame(2, 5,5);
    testGame.printGame();
    
    deque<deque<int>> battleInput;
    battleInput.push_back({0,0});
    battleInput.push_back({1,0});

    cout << "Player 0 card: ";
    cin >> battleInput[0][1];

    while(battleInput[0][1] == 2){
        int temp;
        cout << "Which player do you want to infiltrate: ";
        cin >> temp;
        deque<deque<int>> infiltrateCards = testGame.getInfiltrateCards( 0, temp);
        for( int i = 0; i < 4; i++){
            if(i == 0){
                cout << "Your Deck: ";
            } else if( i == 1){
                cout << "Your Jail: ";
            } else if( i == 1){
                cout << "Your Hand: ";
            } else{
                cout << "Their Hand: ";
            }
            for(int j = 0; j < infiltrateCards[i].size(); j++){
                cout << infiltrateCards[i][j] << ", ";
            }
            cout << endl;
        }
        int card;
        cout << "What card do you want to take? (-1 if no card): ";
        cin >> card;
        if(card != -1){
            testGame.infiltrate(0, temp, card);
        }
        cout << "Please play new card Player 0: ";
        cin >> battleInput[0][1];
    }

    cout << "Player 1 card: ";
    cin >> battleInput[1][1];

    while(battleInput[1][1] == 2){
        int temp;
        cout << "Which player do you want to infiltrate: ";
        cin >> temp;
        deque<deque<int>> infiltrateCards = testGame.getInfiltrateCards( 1, temp);
        for( int i = 0; i < 4; i++){
            if(i == 0){
                cout << "Your Deck: ";
            } else if( i == 1){
                cout << "Your Jail: ";
            } else if( i == 1){
                cout << "Your Hand: ";
            } else{
                cout << "Their Hand: ";
            }
            for(int j = 0; j < infiltrateCards[i].size(); j++){
                cout << infiltrateCards[i][j] << ", ";
            }
            cout << endl;
        }
        int card;
        cout << "What card do you want to take? (-1 if no card): ";
        cin >> card;
        if(card != -1){
            testGame.infiltrate(1, temp, card);
        }
        cout << "Please play new card Player 1: ";
        cin >> battleInput[1][1];
    }

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
    testGame.playerWins(battleOutput[0][0], cardsPlayed);
    cout << "Player " << battleOutput[0][0] << " won with " << battleOutput[0][1] << endl;

}