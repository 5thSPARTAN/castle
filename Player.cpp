#include "Player.h"

// Input player, health
Player::Player(int p, int h, int mh){
    playerNumber = p;
    maxHealth = mh;
    if( mh >= h)
        health = h;
    else
        health = mh;
    
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

Player::~Player(){

}

int Player::getPlayerNumber(){
    return playerNumber;
}
int Player::getPlayerHealth(){
    return health;
}

void Player::damage(){
    health--;
    return;
} // 1 damage
void Player::heal(){
    if(health < maxHealth){
        health++;
    }
    return;
} // 1 heal
int Player::getHealth(){
    return health;
}
int Player::getDeckSize(){
    return deck.size();
}
int Player::getJailSize(){
    return jail.size();
}
int Player::getHandSize(){
    return hand.size();
}

bool Player::isLose(){
    if( health <= 0){
        return true;
    } else if( deck.empty() && hand.empty()){
        return true;
    }
    return false;
}
bool Player::deckEmpty(){
    return deck.empty();
}
bool Player::jailEmpty(){
    return jail.empty();
}
bool Player::handEmpty(){
    return hand.empty();
}
bool Player::warDiscardEmpty(){
    return warDiscard.empty();
}
bool Player::warPlayedEmpty(){
    return warPlayed.empty();
}

void Player::cycleDeckToHand(){
    hand.push_front(deck.back());
    deck.pop_back();
    return;
}
void Player::cycleHandToJail(){
    jail.push_front(hand.back());
    hand.pop_back();
    return;
}
void Player::cycleHandToWarDiscard(){
    warDiscard.push_front(hand.back());
    hand.pop_back();
    return;
}
void Player::cycleWarDiscardToDeck(){
    deck.push_front(warDiscard.back());
    warDiscard.pop_back();
}
void Player::cycleWarDiscardToJail(){
    jail.push_front(warDiscard.back());
    warDiscard.pop_back();
}
void Player::cycleWarPlayedToDeck(){
    deck.push_front(warPlayed.back());
    warPlayed.pop_back();
}
void Player::cycleWarPlayedToJail(){
    jail.push_front(warPlayed.back());
    warPlayed.pop_back();
}
void Player::deckToHand(int card){
    hand.push_front(card);
    deck.erase(remove(deck.begin(),deck.end(),card), deck.end());
    return;
}
void Player::jailToHand(int card){
    hand.push_front(card);
    jail.erase(remove(jail.begin(),jail.end(),card), jail.end());
    return;
}
void Player::handToDeck(int card){
    deck.push_front(card);
    hand.erase(remove(hand.begin(),hand.end(),card), hand.end());
    return;
}
void Player::handToJail(int card){
    jail.push_front(card);
    hand.erase(remove(hand.begin(),hand.end(),card), hand.end());
    return;
}
void Player::handToWarPlayed(int card){
    warPlayed.push_front(card);
    hand.erase(remove(hand.begin(),hand.end(),card), hand.end());
    return;
}

void Player::winWithCard(int card){
    switch (card){
        case 3:
        case 4:
            // nothing else happens
            break;
        case 5:
        case 6:
            jailBreak();
            break;
        case 7:
        case 8:
            heal();
            break;
        case 9:
        case 10:
            // nothing to themselves
            break;
        case 11:
            jailBreak();
            break;
        case 12:
            jailBreak();
            heal();
            heal();
            break;
        case 13:
            jailBreak();
            heal();
            break;
    }

    return;
}

void Player::loseToCard(int card){
    switch (card){
        case 3:
        case 4:
            // nothing else happens
            break;
        case 5:
        case 6:
            discardHand();
            break;
        case 7:
        case 8:
            break;
        case 9:
        case 10:
            damage();
            break;
        case 11:
            damage();
            damage();
            break;
        case 12:
            break;
        case 13:
            damage();
            damage();
            break;
    }

}

void Player::jailBreak(){
    while(jail.size() != 0){
        deck.insert(deck.begin(), jail.back());
        jail.pop_back();
    }
}
void Player::discardHand(){
    for(int i = 0; i < 3; i++){
        if(!deckEmpty()){
            cycleDeckToHand();
        }
        if(!handEmpty()){
            cycleHandToJail();
        }
    }
    return;
}
void Player::war(int card){
    int discardCount = 0;
    handToWarPlayed(card);
    // replace played card in hand
    if(!deck.empty()){
        cycleDeckToHand();
    }

    while(discardCount < 3){
        if(deck.empty() && hand.size() == 1){
            discardCount = 3;
        }
        else{
            cycleHandToWarDiscard();
            if(!deck.empty()){
                cycleDeckToHand();
            }
            discardCount++;
        }
    }
}
deque<int> Player::getDeck(){
    return deck;
}
deque<int> Player::getJail(){
    return jail;
}
deque<int> Player::getHand(){
    return hand;
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

    cout << "warPlayed: ";
    for( int i : warPlayed){
        cout << i << ", ";
    }
    cout << endl;

    cout << "warDiscard: ";
    for( int i : warDiscard){
        cout << i << ", ";
    }
    cout << endl;
}