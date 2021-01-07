# Checkers

Game of [checkers](https://en.wikipedia.org/wiki/Draughts), with alpha-beta pruning playing agent
and different evaluation functions

![checkers_game](https://user-images.githubusercontent.com/32793798/103526931-411ff980-4e8a-11eb-9b85-3313550e9542.gif)

## How to run
You must have python3 installed.  
just type in the terminal `python Game.py` to run the game.  
it's cross-platform, and tested on both ubuntu and windows

## Files Structure
1. `Checkers.py` contains all the functionalities of the checkers game such as move generators,  
   minimax algorithm and evaluation functions. The functions are well documented.
2. `Game.py` contains the functions of the GUI
3. `MinimaxVsMinimax.py` contains code to run minimax agent against another minimax agent with
   different or same parameters.  
   It's just for comparing between different evaluation functions and hyperparameters.
4. `MinimaxVsRandom.py` contains code to run minimax agent against random playing agent.  
   It's for the same purpose as `MinimaxVsMinimax.py`

Refer to the [Report](Checkers%20Report.pdf) for more information about experiment and results

## Configuration
1. You can change the size of the checkers instead of the default 8*8 to any even number greater than 3.
2. You can change the mode of the game, it can be either `Mode.MULTIPLE_PLAYER` or `Mode.SINGLE_PLAYER`
3. You can change the starting player in `Game.py` it can be either `Checkers.BLACK` or `Checkers.WHITE`
4. You can change the algorithm used to play a computer move, it can be either `Algorithm.MINIMAX` or `Algorithm.RANDOM` (minimax is much harder).
### Minimax configuration
1. You can change the `maxDepth`, the higher the max depth the harder the level of play and the more time it takes to compute the play.
2. You can change the evaluation function, it can be either `Checkers.evaluate1`, `Checkers.evaluate2` or `Checkers.endGame`.
   -  `evaluate2` is harder than `evaluate1`
   -  `endGame` is used at the end of the game, when there is no much pieces on the board, it's good for traping and escaping
3. You can set `INCREASE_DEPTH` to `True` or `False`, if it's true, then at the end of the game the max depth will increase, to be able to search more for a solution.