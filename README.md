# Checkers

Game of [checkers](https://en.wikipedia.org/wiki/Draughts), with alpha-beta pruning playing agent
and different evaluation functions

![checkers_game](https://user-images.githubusercontent.com/32793798/103156614-faa80c00-47b2-11eb-9f83-0f5ea874235d.gif)

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

Refer to [Report](Checkers%20Report.pdf) for more information about experiment and results