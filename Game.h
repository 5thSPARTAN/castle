#ifndef GAME_H
#define GAME_H

#include "Player.h"
#include "GameUtils.h"
#include "Observation.h"

class Game{
private:
    deque<Player> players;
    int numberOfPlayers;
    int startingHealth;
    int maxHealth;
    bool infiltrating;
    bool war;
public:
    Game();
    Game(int numberOfPlayers, int startingHealth, int maxHealth);
    ~Game();

    int getNumberOfPlayers();
    int getStartingHealth();
    int getMaxHealth();


    deque<deque<int>> battle(deque<deque<int>> input);
    
    // infiltrator specific functions
    deque<int> infiltrate( int playerPlayed, int playerChosen); //output card #, location (deck(0), jail(1), hand(2))
    void infiltrateSwap(int playerPlayed, int playerChosen, int card, int location);
    void playerWins(int playerNumber, deque<deque<int>> cardsPlayed);

    void printGame();

    //for GameEnv
    Observation toObservation();
    void applyAction(deque<int> action);
    bool isLose(int player);
    bool isOver();
    

};

#endif