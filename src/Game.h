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
    int infiltratingPlayer;
    int infiltratedPlayer;
    int extractedCard;
    int extractedCardLocation;
    bool war;
public:
    Game() = default;
    // numberOfPlayers, startingHealth, maxHealth
    Game(int np, int sh, int mh);
    ~Game() = default;

    int getNumberOfPlayers() const;
    int getStartingHealth()const;
    int getMaxHealth() const;
    int getNumberOfPlayersLeft() const;


    deque<deque<int>> battle(deque<deque<int>>& input);
    
    // infiltrator specific functions
    deque<int> infiltrate( int playerPlayed, int playerChosen); //output card #, location (deck(0), jail(1), hand(2))
    void infiltrateSwap(int playerPlayed, int playerChosen, int card, int location);
    void playerWins(int playerNumber, deque<deque<int>> cardsPlayed);

    //for GameEnv
    Observation toObservation(int playerNumber) const;
    void applyAction(deque<int> action);
    bool isWin(int player) const;
    bool isLose(int player) const;
    bool isOver() const;
    
/* for testing
    void printGame();
*/
};

#endif