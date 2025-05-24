#ifndef GAME_H
#define GAME_H

#include "Player.h"
#include "GameUtils.h"

class Game{
private:
    deque<Player> players;
    int turnCounter;
    bool war;
public:
    Game(int numberOfPlayers, int startingHealth, int maxHealth);
    ~Game();

    deque<deque<int>> battle(deque<deque<int>> input);
    
    // infiltrator specific functions
    deque<deque<int>> getInfiltrateCards(int playerPlayed, int playerChosen); // also moves 2 to the jail
    void infiltrate( int playerPlayed, int playerChosen, int card);

    void playerWins(int playerNumber, deque<deque<int>> cardsPlayed);
    void cardWins( int playerNumber, int cardPlayed);

    void printGame();
};

#endif