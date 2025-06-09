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
    static deque<int> shuffleDeck();

    // playerNumber, health, maxHealth
    Player(int p, int h, int mh);
    ~Player();

    int getPlayerNumber() const;
    int getPlayerHealth() const;

    void damage(); // 1 damage
    void heal(); // 1 heal
    int getHealth() const;
    int getDeckSize() const;
    int getJailSize() const;
    int getHandSize() const;

    bool isLose() const;
    bool deckEmpty() const;
    bool jailEmpty() const;
    bool handEmpty() const;
    bool warDiscardEmpty() const;
    bool warPlayedEmpty() const;
    bool handContains(int card) const;

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

    
    deque<int> getDeck() const;
    deque<int> getJail() const;
    deque<int> getHand() const;
    deque<int> getWarPlayed() const;

    /* for testing
    void printPlayer() const;
    */

};

#endif