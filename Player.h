#ifndef PLAYER_H
#define PLAYER_H

#include <deque>
#include <random> // for random
#include <algorithm> // for shuffle
using namespace std;

// for testing
#include <iostream>


class Player{
private:
    deque<int> deck;
    deque<int> jail;
    deque<int> hand;
    deque<int> warDiscard;
    deque<int> warPlayed;
    int playerNumber;
    int health;
    int maxHealth;

public:
    Player(int playerNumber, int health, int maxHealth);
    ~Player();

    int getPlayerNumber();
    int getPlayerHealth();

    void damage(); // 1 damage
    void heal(); // 1 heal
    int getHealth();
    int getDeckSize();
    int getJailSize();
    int getHandSize();

    bool isLose();
    bool deckEmpty();
    bool jailEmpty();
    bool handEmpty();
    bool warDiscardEmpty();
    bool warPlayedEmpty();
    bool handContains(int card);

    void cycleDeckToHand();
    void cycleHandToJail();
    void cycleHandToWarDiscard();
    void cycleWarDiscardToDeck();
    void cycleWarDiscardToJail();
    void cycleWarPlayedToDeck();
    void cycleWarPlayedToJail();

    void deckToHand(int card);
    void jailToHand(int card);
    void handToDeck(int card);
    void handToJail(int card);
    void handToWarPlayed(int card);
    
    void winWithCard(int card);
    void loseToCard(int card);

    void jailBreak();
    // discards up to 3 cards depending on deck
    void discardHand();
    void war(int card);

    
    deque<int> getDeck();
    deque<int> getJail();
    deque<int> getHand();

    void printPlayer();

};

#endif