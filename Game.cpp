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
int Game::getNumberOfPlayersLeft(){
    int count = 0;
    for( Player& p: players){
        if(!p.isLose()){
            count++;
        }
    }
    return count;
}


deque<deque<int>> Game::battle(deque<deque<int>> input){
    deque<deque<int>> winners = findWinners(input);
    if( winners.size() > 1){
        // war has occured
        for( deque<int>& i : winners){
            players[i[0]].war(winners[0][1]);
        }
        war = true;
        return winners;
    }
    else{
        war = false;
        return winners;
    }

}

void Game::playerWins(int playerNumber, deque<deque<int>> cardsPlayed){
    deque<int> winningCards;
    for(deque<int>& i : cardsPlayed){
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
            for(int& wc : winningCards){
                for( int& pc : p.getHand()){
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
            for(deque<int>& cp: cardsPlayed){
                if( cp[0] == p.getPlayerNumber()){
                    p.handToJail(cp[1]);
                    if(!p.deckEmpty()){
                        p.cycleDeckToHand();
                    }
                }
            }
            for(int& wc : winningCards){
                p.loseToCard(wc);
            }
        }
    }

}
  
deque<int> Game::infiltrate( int playerPlayed, int playerChosen){
    // move 2 to jail
    players[playerPlayed].handToJail(2);

    
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> dist(0, players[playerChosen].getHandSize()-1);
    int card = players[playerChosen].getHand()[dist(gen)];

    for( int& i : players[playerPlayed].getDeck()){
        if( card == i){
            return {card, 0};
        }
    }
    for( int& i : players[playerPlayed].getJail()){
        if( card == i){
            return {card, 1};
        }
    }
    for( int& i : players[playerPlayed].getHand()){
        if( card == i){
            return {card, 2};
        }
    }
    return {};
}

void Game::infiltrateSwap( int playerPlayed, int playerChosen, int card, int location){
    if( location == 0){
        players[playerChosen].handToDeck(card);
        if(!players[playerChosen].deckEmpty()){
            players[playerChosen].cycleDeckToHand();
        }
        players[playerPlayed].deckToHand(card);
        return;
    } else if( location == 1){
        players[playerChosen].handToJail(card);
        if(!players[playerChosen].deckEmpty()){
            players[playerChosen].cycleDeckToHand();
        }
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

Observation Game::toObservation(int playerNumber){
    Observation output;
    // features
    output.features.push_back(static_cast<float>(playerNumber));
    output.features.push_back(static_cast<float>(getNumberOfPlayersLeft()));
    output.features.push_back(static_cast<float>(getMaxHealth()));
    output.features.push_back(static_cast<float>(players[0].getHealth()));
    output.features.push_back(static_cast<float>(players[0].getDeckSize()));
    output.features.push_back(static_cast<float>(players[0].getJailSize()));
    output.features.push_back(static_cast<float>(players[0].getHandSize()));
    output.features.push_back(static_cast<float>(players[1].getHealth()));
    output.features.push_back(static_cast<float>(players[1].getDeckSize()));
    output.features.push_back(static_cast<float>(players[1].getJailSize()));
    output.features.push_back(static_cast<float>(players[1].getHandSize()));
    output.features.push_back(static_cast<float>(players[2].getHealth()));
    output.features.push_back(static_cast<float>(players[2].getDeckSize()));
    output.features.push_back(static_cast<float>(players[2].getJailSize()));
    output.features.push_back(static_cast<float>(players[2].getHandSize()));
    output.features.push_back(static_cast<float>(players[3].getHealth()));
    output.features.push_back(static_cast<float>(players[3].getDeckSize()));
    output.features.push_back(static_cast<float>(players[3].getJailSize()));
    output.features.push_back(static_cast<float>(players[3].getHandSize()));
    output.features.push_back(static_cast<float>(war));
    output.features.push_back(static_cast<float>(infiltrating));

    if(infiltrating){
        output.features.push_back(static_cast<float>(infiltratedPlayer));
    } else {
        output.features.push_back(static_cast<float>(-1));
    }
    
    if(infiltrating){
        output.features.push_back(static_cast<float>(extractedCardLocation));
    } else {
        output.features.push_back(static_cast<float>(-1));
    }


    // action mask
    if(players[playerNumber].isLose()){
        output.actionMask.push_back(true);
        for( int i = 1; i < 29; i++){
            output.actionMask.push_back(false);
        }
    } else if(infiltrating){
        if(infiltratingPlayer == playerNumber){
            output.actionMask.push_back(false);
            output.actionMask.push_back(true);
            for( int i = 2; i < 14; i++){
                if( extractedCard == i){
                    output.actionMask.push_back(true);
                } else {
                    output.actionMask.push_back(false);
                }
            }

            for( int i = 14; i < 29; i++){
                output.actionMask.push_back(false);
            }
        } else {
            output.actionMask.push_back(true);
            for( int i = 1; i < 29; i++){
                output.actionMask.push_back(false);
            }
        }
    } else if(war){
        if( players[playerNumber].warDiscardEmpty() && players[playerNumber].warPlayedEmpty()){
            output.actionMask.push_back(true);
            for( int i = 0; i < 28; i++){
                output.actionMask.push_back(false);
            }
        } else {
            if(players[playerNumber].handEmpty()){
                output.actionMask.push_back(true);
            } else {
                output.actionMask.push_back(false);
            }
            for( int i = 1; i < 14; i++){
                output.actionMask.push_back(false);
            }
            output.actionMask.push_back(players[playerNumber].handContains(3));
            output.actionMask.push_back(players[playerNumber].handContains(4));
            output.actionMask.push_back(players[playerNumber].handContains(5));
            output.actionMask.push_back(players[playerNumber].handContains(6));
            output.actionMask.push_back(players[playerNumber].handContains(7));
            output.actionMask.push_back(players[playerNumber].handContains(8));
            output.actionMask.push_back(players[playerNumber].handContains(9));
            output.actionMask.push_back(players[playerNumber].handContains(10));
            output.actionMask.push_back(players[playerNumber].handContains(11));
            output.actionMask.push_back(players[playerNumber].handContains(12));
            output.actionMask.push_back(players[playerNumber].handContains(13));
            if( players[playerNumber].handContains(2) ){
                for( int i = 0 ; i < 4; i ++){
                    if(playerNumber == i || players[i].isLose()){
                        output.actionMask.push_back(false);
                    } else {
                        output.actionMask.push_back(true);
                    }
                }
            } else {
                for( int i = 0; i < 4;i++){
                    output.actionMask.push_back(false);
                }
            }
        }
    } else {
        if(!players[playerNumber].isLose()){
            for( int i = 0; i < 14; i++){
                output.actionMask.push_back(false);
            }
            output.actionMask.push_back(players[playerNumber].handContains(3));
            output.actionMask.push_back(players[playerNumber].handContains(4));
            output.actionMask.push_back(players[playerNumber].handContains(5));
            output.actionMask.push_back(players[playerNumber].handContains(6));
            output.actionMask.push_back(players[playerNumber].handContains(7));
            output.actionMask.push_back(players[playerNumber].handContains(8));
            output.actionMask.push_back(players[playerNumber].handContains(9));
            output.actionMask.push_back(players[playerNumber].handContains(10));
            output.actionMask.push_back(players[playerNumber].handContains(11));
            output.actionMask.push_back(players[playerNumber].handContains(12));
            output.actionMask.push_back(players[playerNumber].handContains(13));
            if( players[playerNumber].handContains(2) ){
                for( int i = 0 ; i < 4; i ++){
                    if(playerNumber == i || players[i].isLose()){
                        output.actionMask.push_back(false);
                    } else {
                        output.actionMask.push_back(true);
                    }
                }
            } else {
                for( int i = 0; i < 4;i++){
                    output.actionMask.push_back(false);
                }
            }
        }
    }
    return output;

}

void Game::applyAction(deque<int> action){
    if(infiltrating){
        if( action[infiltratingPlayer] <=13 && action[infiltratingPlayer] >=2 ){
            int location = -1;
            for( int& j : players[infiltratingPlayer].getDeck()){
                if( j == action[infiltratingPlayer]){
                    location = 0;
                    infiltrateSwap(infiltratingPlayer, infiltratedPlayer, action[infiltratingPlayer], 0);
                    break;
                }
            }
            if( location != 0 ){
                for( int& j : players[infiltratingPlayer].getJail()){
                    if( j == action[infiltratingPlayer]){
                        infiltrateSwap(infiltratingPlayer, infiltratedPlayer, action[infiltratingPlayer], 1);
                        break;
                    }
                }
            }
        }
        while(players[infiltratingPlayer].getHandSize() < 3 && !players[infiltratingPlayer].deckEmpty()){
            players[infiltratingPlayer].cycleDeckToHand();
        }
        infiltrating = false;
    } else {
        deque<deque<int>> battleInput;
        for(int i = 0; i < action.size(); i++){
            switch(action[i]){
                case 14:
                    battleInput.push_back({i,3});
                    break;
                case 15:
                    battleInput.push_back({i,4});
                    break;
                case 16:
                    battleInput.push_back({i,5});
                    break;
                case 17:
                    battleInput.push_back({i,6});
                    break;
                case 18:
                    battleInput.push_back({i,7});
                    break;
                case 19:
                    battleInput.push_back({i,8});
                    break;
                case 20:
                    battleInput.push_back({i,9});
                    break;
                case 21:
                    battleInput.push_back({i,10});
                    break;
                case 22:
                    battleInput.push_back({i,11});
                    break;
                case 23:
                    battleInput.push_back({i,12});
                    break;
                case 24:
                    battleInput.push_back({i,13});
                    break;
                case 25:
                    if(i != 0){
                        infiltrating = true;
                        infiltratingPlayer = i;
                        infiltratedPlayer = 0;
                        deque<int> dataExtracted = infiltrate( i,0);
                        extractedCard = dataExtracted[0];
                        extractedCardLocation = dataExtracted[1];
                        
                    }
                    return;
                case 26:
                    if(i != 1){
                        infiltrating = true;
                        infiltratingPlayer = i;
                        infiltratedPlayer = 1;
                        deque<int> dataExtracted = infiltrate( i,1);
                        extractedCard = dataExtracted[0];
                        extractedCardLocation = dataExtracted[1];
                    }
                    return;
                case 27:
                    if(i != 2){
                        infiltrating = true;
                        infiltratingPlayer = i;
                        infiltratedPlayer = 2;
                        deque<int> dataExtracted = infiltrate( i,2);
                        extractedCard = dataExtracted[0];
                        extractedCardLocation = dataExtracted[1];
                    }
                    return;
                case 28:
                    if(i != 3){
                        infiltrating = true;
                        infiltratingPlayer = i;
                        infiltratedPlayer = 3;
                        deque<int> dataExtracted = infiltrate( i,3);
                        extractedCard = dataExtracted[0];
                        extractedCardLocation = dataExtracted[1];
                    }
                    return;
                default:                    
                    break;
            }
        }
        deque<deque<int>> battleOutput;
        if( battleInput.size() == 0){
            return;
        } else if( battleInput.size() == 1){
            battleOutput = battleInput;   
        } else {
            battleOutput = battle(battleInput);
        }
        if(battleOutput.size() > 1){
            return;
        }
        for( int& card: players[battleOutput[0][0]].getWarPlayed()){
            battleInput.push_back({battleOutput[0][0], card});
        }
        playerWins(battleOutput[0][0], battleInput);
    }
}
bool Game::isWin(int player){
    for( int i = 0; i < numberOfPlayers; i++){
        if( i == player){
            if(players[i].isLose()){
                return false;
            }
        } else {
            if(!players[i].isLose()){
                return false;
            }
        }
    }
    return true;
}
bool Game::isLose(int player){
    return players[player].isLose();
}
bool Game::isOver(){
    int count = 0;
    for( Player& p :players){
        if(p.isLose() == true){
            count++;
        }
    }
    if( count >= numberOfPlayers - 1){
        return true;
    }
    return false;
}