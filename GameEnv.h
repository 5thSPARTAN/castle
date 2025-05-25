#include "Game.h"
#include "Observation.h"
#include <tuple>

class GameEnv{
private:
    Game game_;
    int players;
    int startingHealth;
    int maxHealth;
public:
    GameEnv(int players, int startingHealth, int maxHealth);
    ~GameEnv();


    void reset();
    tuple<deque<Observation>, deque<float>, bool> step(deque<int> action);

}