#include "Game.h"

Game::Game(){}

Game::Game(int numberOfPlayers, int startingHealth, int maxHealth){
    for( int i = 0; i < numberOfPlayers; i++){
        players.push_back(Player(i, startingHealth, maxHealth));
    }
    turnCounter = 0;
    war = false;
}

Game::~Game(){

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


deque<deque<int>> Game::getInfiltrateCards(int playerPlayed, int playerChosen){
    players[playerPlayed].handToJail(2);
    players[playerPlayed].cycleDeckToHand();
    
    deque<deque<int>> output; // Player Played deck, jail, hand, playerchosen hand
    output.push_back(players[playerPlayed].getDeck());
    output.push_back(players[playerPlayed].getJail());
    output.push_back(players[playerPlayed].getHand());
    output.push_back(players[playerChosen].getHand());    

    return output;
}
  
void Game::infiltrate( int playerPlayed, int playerChosen, int card){
    for( int i : players[playerPlayed].getDeck()){
        if( i == card){
            players[playerChosen].handToDeck(card);
            players[playerPlayed].deckToHand(card);
            return;
        }
    }
    for( int i : players[playerPlayed].getJail()){
        if( i == card){
            players[playerChosen].handToJail(card);
            players[playerPlayed].jailToHand(card);
            return;
        }
    }
    for( int i : players[playerPlayed].getHand()){
        if( i == card){
            return;
        }
    }
}

void Game::printGame(){
    for( Player p : players){
        p.printPlayer();
        cout << endl;
    }
}