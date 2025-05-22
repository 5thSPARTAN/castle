#include "Player.h"

// Input player, health
Player::Player(int p, int h){
    playerNumber = p;
    health = h;
    
    deck = {2,3,4,5,6,7,8,9,10,11,12,13};
    
    // shuffle deck
    random_device rd;
    mt19937 g(rd());
    shuffle(deck.begin(), deck.end(), g);

    for(int i = 0; i < 3; i++){
        hand.push_back(deck.back());
        deck.pop_back();
    }
}

void Player::printPlayer(){
    cout << "Player " << playerNumber << endl;
    cout << "Health: " << health << endl;
       
    cout << "Deck: ";
    for( int i : deck){
        cout << i << ", ";
    }
    cout << endl;

    cout << "jail: ";
    for( int i : jail){
        cout << i << ", ";
    }
    cout << endl;

    cout << "hand: ";
    for( int i : hand){
        cout << i << ", ";
    }
    cout << endl;
}