#include "Game.h"

Game::Game(){}

Game::Game(int np, int sh, int mh){
    numberOfPlayers = np;
    startingHealth = sh;
    maxHealth = mh;
    for( int i = 0; i < numberOfPlayers; i++){
        players.push_back(Player(i, startingHealth, maxHealth));
    }
    infiltrating = false;
    war = false;
}

Game::~Game(){}

int Game::getNumberOfPlayers(){
    return numberOfPlayers;
}
int Game::getStartingHealth(){
    return startingHealth;
}
int Game::getMaxHealth(){
    return maxHealth;
}



deque<deque<int>> Game::battle(deque<deque<int>> input){
    deque<deque<int>> winners = findWinners(input);
    if( winners.size() > 1){
        // war has occured
        for( deque<int> i : winners){
            players[i[0]].war(winners[0][1]);
        }
        return winners;
    }
    else{
        return winners;
    }

}

void Game::playerWins(int playerNumber, deque<deque<int>> cardsPlayed){
    deque<int> winningCards;
    for(deque<int> i : cardsPlayed){
        if(i[0] == playerNumber){
            winningCards.push_back(i[1]);
        }
    }

    for(Player &p : players){
        if(p.getPlayerNumber() == playerNumber){
            while(!p.warPlayedEmpty()){
                p.cycleWarPlayedToDeck();
            }
            while(!p.warDiscardEmpty()){
                p.cycleWarDiscardToDeck();
            }
            // check if winning cards are in players hand
            for(int wc : winningCards){
                for( int pc : p.getHand()){
                    if( wc == pc){
                        p.handToDeck(wc);
                        if(!p.deckEmpty()){
                            p.cycleDeckToHand();
                        }                        
                    }
                }
                p.winWithCard(wc);
            }
        } else {
            while(!p.warPlayedEmpty()){
                p.cycleWarPlayedToJail();
            }
            while(!p.warDiscardEmpty()){
                p.cycleWarDiscardToJail();
            }
            // check if losing card is in players hand
            for(deque<int> cp: cardsPlayed){
                if( cp[0] == p.getPlayerNumber()){
                    p.handToJail(cp[1]);
                    if(!p.deckEmpty()){
                        p.cycleDeckToHand();
                    }
                }
            }
            for(int wc : winningCards){
                p.loseToCard(wc);
            }
        }
    }

}
  
deque<int> Game::infiltrate( int playerPlayed, int playerChosen){
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> dist(0, players[playerChosen].getHandSize()-1);
    int card = players[playerChosen].getHand()[dist(gen)];

    for( int i : players[playerPlayed].getDeck()){
        if( card == i){
            return {card, 0};
        }
    }
    for( int i : players[playerPlayed].getJail()){
        if( card == i){
            return {card, 1};
        }
    }
    for( int i : players[playerPlayed].getHand()){
        if( card == i){
            return {card, 2};
        }
    }

}

void Game::infiltrateSwap( int playerPlayed, int playerChosen, int card, int location){
    if( location == 0){
        players[playerChosen].handToDeck(card);
        players[playerPlayed].deckToHand(card);
        return;
    } else if( location == 1){
        players[playerChosen].handToJail(card);
        players[playerPlayed].jailToHand(card);
        return;
    }
}

void Game::printGame(){
    for( Player p : players){
        p.printPlayer();
        cout << endl;
    }
}

void Game::applyAction(deque<int> action){
    if(infiltrating){
        
    }
}
bool Game::isLose(int player){
    return players[player].isLose();
}
bool Game::isOver(){
    int count = 0;
    for( Player p :players){
        if(p.isLose() == true){
            count++;
        }
    }
    if( count >= numberOfPlayers - 1){
        return true;
    }
    return false;
}