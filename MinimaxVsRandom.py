from Checkers import Checkers

wins = 0
draws = 0
games = 1000
START_PLAYER = Checkers.BLACK

for i in range(games):
    game = Checkers()
    # game.printBoard()

    player = START_PLAYER
    cnt = 0
    # statesCounter = {}
    # state = None
    while cnt < 100:
        # state = game.encodeBoard()
        # if state not in statesCounter:
        #     statesCounter[state] = 0
        # statesCounter[state] += 1
        # # the exact same state repeated 3 times -> draw
        # if statesCounter[state] == 3:
        #     print("state repeated 3 times")
        #     break

        evaluate = Checkers.evaluate2
        if cnt > 25:
            evaluate = Checkers.endGame

        if player == START_PLAYER:
            cont, reset = game.minimaxPlay(player, maxDepth=2, evaluate=evaluate, enablePrint=False)
            if not cont:
                break
        else:
            cont, reset = game.randomPlay(player, enablePrint=False)
            if not cont:
                break
        player = 1-player
        cnt += 1
        if reset:
            cnt = 0

    # if stateCounter[state] == 3:
    #     print("Draw")
    #     draws += 1

    if cnt == 100:
        # print("Draw")
        draws += 1
    else:
        # print (("WHITE" if player == Checkers.BLACK else "BLACK") + " Player wins")
        if player != START_PLAYER:
            wins += 1
    print(i, end='\r')

loses = games - wins - draws
print(f"total wins of {wins}/{games}, draws of {draws}/{games} and loses of {loses}/{games}")
