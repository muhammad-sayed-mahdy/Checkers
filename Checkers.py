from collections import Counter
import random
from typing import Callable, List, Tuple
from copy import deepcopy

Board = List[List[int]]
Position = Tuple[int, int]
Positions = List[Position]
Moves = List[Tuple[Position, Positions]]


class Checkers(object):
    """
    checkers class contains methods to play checkers
    """

    WHITE = 1
    WHITE_MAN = 1
    WHITE_KING = 3
    BLACK = 0
    BLACK_MAN = 2
    BLACK_KING = 4
    DX = [1, 1, -1, -1]
    DY = [1, -1, 1, -1]
    OO = 10 ** 9

    def __init__(self, size: int = 8) -> None:
        """Make the initial board of the game

        Args:
            size (int, optional): size of the checkers board. Defaluts to 8.
        Raises:
            Exception: if the size is not even or less than 4
        """
        if size % 2 != 0 or size < 4:
            raise Exception("The size of the board must be even and graeter than 3")

        self.size = size
        self.board = []
        piece = self.WHITE_MAN
        for i in range(size):
            l = []
            f = i % 2 == 1
            if i == size / 2 - 1:
                piece = 0
            elif i == size / 2 + 1:
                piece = self.BLACK_MAN
            for _ in range(size):
                if f:
                    l.append(piece)
                else:
                    l.append(0)
                f = not f
            self.board.append(l)

        self.stateCounter = Counter()

    def printBoard(self, x: int = None, y: int = None):
        """Print the game board in stdout, the given position is printed in green

        Args:
            x (int, optional): the new x position of the recently played move. Defaults to None.
            y (int, optional): the new y position of the recently played move. Defaults to None.
        """
        for i in range(self.size):
            for j in range(self.size):
                if i == x and j == y:
                    print("\033[92m", end="")

                if self.board[i][j] == 0:
                    print("-", end=" ")
                else:
                    print(self.board[i][j], end=" ")

                if i == x and j == y:
                    print("\033[0m", end="")
            print()

    def encodeBoard(self) -> int:
        """Encode the game board so that each state can be represented by a single unique integer

        Returns:
            int: the value of the encoded game board
        """
        value = 0
        for i in range(self.size):
            for j in range(self.size):
                # make the minimum value = 5, 
                # so that it's greater than greatest value of the board (4)
                num = i * self.size + j + 5
                value += num * self.board[i][j]
        return value

    def getBoard(self):
        """Get Game board

        Returns:
            Board: game board
        """
        return deepcopy(self.board)

    def setBoard(self, board: Board):
        """Set game board

        Args:
            board (Board): board to set the game borad to
        """
        self.board = deepcopy(board)

    def isValid(self, x: int, y: int) -> bool:
        """Check if the given position is inside the board

        Args:
            x (int): x position
            y (int): y position

        Returns:
            bool: the given position is valid
        """
        return x >= 0 and x < self.size and y >= 0 and y < self.size

    def nextPositions(self, x: int, y: int) -> Tuple[Positions, Positions]:
        """Get the possible next positions for a given position

        Args:
            x (int): x position
            y (int): y position

        Returns:
            (Positions, Positions): next normal positions, next capture positions
        """
        if self.board[x][y] == 0:
            return []

        player = self.board[x][y] % 2
        captureMoves = []
        normalMoves = []
        sign = 1 if player == self.WHITE else -1
        # only forward for men and both forward and backward for Kings
        rng = 2 if self.board[x][y] <= 2 else 4
        for i in range(rng):
            nx = x + sign * self.DX[i]
            ny = y + sign * self.DY[i]
            if self.isValid(nx, ny):
                if self.board[nx][ny] == 0:
                    normalMoves.append((nx, ny))
                elif self.board[nx][ny] % 2 == 1 - player:
                    nx += sign * self.DX[i]
                    ny += sign * self.DY[i]
                    if self.isValid(nx, ny) and self.board[nx][ny] == 0:
                        captureMoves.append((nx, ny))

        return normalMoves, captureMoves

    def nextMoves(self, player: int) -> Moves:
        """Get the next moves of the game board for a certian player

        Args:
            player (int): the type of player (WHITE, BLACK)

        Returns:
            Moves: valid moves for the player
        """
        captureMoves = []
        normalMoves = []
        for x in range(self.size):
            for y in range(self.size):
                if self.board[x][y] != 0 and self.board[x][y] % 2 == player:
                    normal, capture = self.nextPositions(x, y)
                    if len(normal) != 0:
                        normalMoves.append(((x, y), normal))
                    if len(capture) != 0:
                        captureMoves.append(((x, y), capture))
        if len(captureMoves) != 0:
            return captureMoves
        return normalMoves

    def playMove(self, x: int, y: int, nx: int, ny: int) -> Tuple[bool, int, bool]:
        """Change the board by playing a move from (x, y) to (nx, ny)

        Args:
            x (int): the old x position
            y (int): the old y position
            nx (int): the new x position
            ny (int): the new y position

        Returns:
            canCapture (bool): if the player can capture more pieces.  
            removed (int): the removed piece (if any).  
            promoted (bool) if the current piece is promoted).  
        """
        self.board[nx][ny] = self.board[x][y]
        self.board[x][y] = 0

        removed = 0
        if abs(nx - x) == 2:  # capture move
            dx = nx - x
            dy = ny - y
            removed = self.board[x + dx // 2][y + dy // 2]
            self.board[x + dx // 2][y + dy // 2] = 0  # remove captured piece

        # promote to king
        if self.board[nx][ny] == self.WHITE_MAN and nx == self.size - 1:
            self.board[nx][ny] = self.WHITE_KING
            return False, removed, True
        if self.board[nx][ny] == self.BLACK_MAN and nx == 0:
            self.board[nx][ny] = self.BLACK_KING
            return False, removed, True

        if abs(nx - x) != 2:
            return False, removed, False

        return True, removed, False

    def undoMove(self, x: int, y: int, nx: int, ny: int, removed=0, promoted=False):
        """Undo a move and return the board to its previous state

        Args:
            x (int): the old x position of the played move
            y (int): the old y position of the played move
            nx (int): the new x position of the played move
            ny (int): the new y position of the played move
            removed (int, optional): the removed piece (if any). Defaults to 0.
            promoted (bool, optional): if the played piece was recently promoted. Defaults to False.
        """
        if promoted:
            if self.board[nx][ny] == self.WHITE_KING:
                self.board[nx][ny] = self.WHITE_MAN

            if self.board[nx][ny] == self.BLACK_KING:
                self.board[nx][ny] = self.BLACK_MAN

        self.board[x][y] = self.board[nx][ny]
        self.board[nx][ny] = 0

        if abs(nx - x) == 2:
            dx = nx - x
            dy = ny - y
            self.board[x + dx // 2][y + dy // 2] = removed

    def randomPlay(
        self, player: int, moves: Moves = None, enablePrint=True
    ) -> Tuple[bool, bool]:
        """play a random play for a given player, 
        if the player should continue capturing, then it will

        Args:
            board (Board): the game board
            player (int): the type of the player (WHITE, BLACK)
            moves (Moves, optional): the next moves 
                (used in case of continuing capturing). Defaults to None
            enablePrint (bool, optional): when true the function prints 
                the board after playing. Defaults to True

        Returns:
            continue (bool): false if there is no further plays.  
            reset (bool): true when there is a captured piece, 
                used to reset the counter of the draw condition.  
        """
        if moves == None:
            moves = self.nextMoves(player)
        if len(moves) == 0:
            if enablePrint:
                print(("WHITE" if player == self.BLACK else "BLACK") + " Player wins")
            return False, False
        randomMove = random.choice(moves)
        x, y = randomMove[0]
        nx, ny = random.choice(randomMove[1])

        if enablePrint:
            print(f"Move from ({x}, {y}) to ({nx}, {ny})")
        canCapture, removed, _ = self.playMove(x, y, nx, ny)
        if enablePrint:
            self.printBoard(nx, ny)

        if canCapture:
            _, nextCaptures = self.nextPositions(nx, ny)
            if len(nextCaptures) != 0:
                self.randomPlay(
                    player, [((nx, ny), nextCaptures)], enablePrint=enablePrint
                )

        reset = removed != 0
        return True, reset

    def evaluate1(self, maximizer: int) -> int:
        """evaluate the current state of the board

        Args:
            maximizer (int): the type of the maximizer player (WHITE, BLACK)

        Returns:
            int: score of the board
        """
        # score = (2*maximizer_kings+maximizer_men - (2*opponent_kings + opponent_men))*1000
        
        score = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != 0:
                    if self.board[i][j] % 2 == maximizer:
                        score += (self.board[i][j] + 1) // 2
                    else:
                        score -= (self.board[i][j] + 1) // 2
        return score * 1000

    def cellContains(self, x: int, y: int, player: int) -> bool:
        """return if cell at (x, y) contains player

        Args:
            x (int): x position of cell
            y (int): y position of cell
            player (int): type of player (WHITE/BLACK)

        Returns:
            bool: if cell at (x, y) contains player
        """
        return self.board[x][y] != 0 and self.board[x][y] % 2 == player

    def endGame(self, maximizer: int) -> int:
        """evaluate the current state of the board based on end game strategies
            between maximizer player and the opponent

        Args:
            maximizer (int): the type of the maximizer player (WHITE, BLACK)

        Returns:
            int: score of the board
        """
        score1 = 0
        score2 = 0
        maxPieces = 0
        minPieces = 0
        rowScore = 0
        base = 0 if maximizer == self.WHITE else self.size-1
        minimizer = 1 - maximizer
        minimizerPositions = []
        for x in range(self.size):
            for y in range(self.size):
                if self.cellContains(x, y, minimizer):
                    minimizerPositions.append((x, y))

        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != 0:
                    if self.board[i][j] % 2 == maximizer:
                        maxPieces += 1
                        if (self.board[i][j] + 1) // 2 == 1:
                            rowScore += abs(base-i)
                        score1 += (self.board[i][j] + 1) // 2
                        for x,y in minimizerPositions:
                            score2 += (x-i)**2 + (y-j)**2
                    else:
                        minPieces += 1
                        score1 -= (self.board[i][j] + 1) // 2

        # penalize if the minimizer is in the corner to be able to trap him at the end of the game                   
        minimizerCorner = 0
        for x, y in minimizerPositions:
            if (x,y) == (0, 1) or (x,y) == (1, 0) or (x, y) == (self.size-1, self.size-2) \
                or (x,y) == (self.size-2, self.size-1):
                minimizerCorner = 1

        maximizerCorner = 0
        if self.cellContains(0, 1, maximizer) or self.cellContains(1, 0, maximizer) \
            or self.cellContains(self.size-1, self.size-2, maximizer) \
            or self.cellContains(self.size-2, self.size-1, maximizer):
            maximizerCorner = 1

        if maxPieces > minPieces:   #come closer to opponent
            return score1*1000 - score2 - minimizerCorner*5 + rowScore*10
        else:    # run away
            return score1*1000 + score2 + maximizerCorner*5

    def evaluate2(self, maximizer: int) -> int:
        """evaluate the current state of the board

        Args:
            maximizer (int): the type of the maximizer player (WHITE, BLACK)

        Returns:
            int: score of the board
        """
        
        men = 0
        kings = 0
        backRow = 0
        middleBox = 0
        middleRow = 0
        vulnerable = 0
        protected = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != 0:
                    sign = 1 if self.board[i][j] % 2 == maximizer else -1
                    if self.board[i][j] <= 2:
                        men += sign*1
                    else:
                        kings += sign*1
                    if sign == 1 and ((i == 0 and maximizer == self.WHITE) or (i == self.size-1 and maximizer == self.BLACK)):
                        backRow += 1
                    if i == self.size/2-1 or i == self.size/2:
                        if j >= self.size/2-2 and j < self.size/2+2:
                            middleBox += sign*1
                        else:
                            middleRow += sign*1

                    myDir = 1 if maximizer == self.WHITE else -1
                    vul = False
                    for k in range(4):
                        x = i + self.DX[k]
                        y = j + self.DY[k]
                        n = i - self.DX[k]
                        m = j - self.DY[k]
                        opDir = abs(x-n)/(x-n)
                        if self.isValid(x, y) and self.board[x][y] != 0 and self.board[x][y] % 2 != maximizer \
                            and self.isValid(n, m) and self.board[n][m] == 0 and (self.board[x][y] > 2 or myDir != opDir):
                            vul = True
                            break
                    
                    if vul:
                        vulnerable += sign*1
                    else:
                        protected += sign*1
                
        return men*2000 + kings*4000 + backRow*400 + middleBox*250 + middleRow*50 - 300*vulnerable + 300*protected

    def stateValue(self, maximizer: int) -> int:
        """get value of the board state,
        when the maximizer's pieces is greater than the minimizer's, 
        penalize repeating the same state

        Args:
            maximizer (int): the type of the maximizer player (WHIET/BLACK)

        Returns:
            int: value of the board state
        """
        maxPieces = 0
        minPieces = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != 0:
                    if self.board[i][j] % 2 == maximizer:
                        maxPieces += 1
                    else:
                        minPieces += 1
        if (maxPieces > minPieces):
            return -self.stateCounter[self.encodeBoard()]
        return 0

    def minimax(
        self,
        player: int,
        maximizer: int,
        depth: int = 0,
        alpha: int = -OO,
        beta: int = OO,
        maxDepth: int = 4,
        evaluate: Callable[[int], int] = evaluate2,
        moves: Moves = None,
    ) -> int:
        """Get the score of the board using alpha-beta algorithm

        Args:
            player (int): the type of the current player (WHITE, BLACK)
            maximizer (int): the type of the maximizer player (WHITE, BLACK)
            depth (int, optional): the current depth of the algorithm. Defaults to 0.
            alpha (int, optional): the value of alpha. Defaults to -OO.
            beta (int, optional): the value of beta of the algorithm. Defaults to OO.
            maxDepth (int, optional): the higher the max depth, 
                the harder the level of th play and the more time the algorithm will take. Defaults to 4.
            evaluate (Callable[[int], int], optional): evaluation function. Defaults to evaluate2
            moves (Moves, optional): the next capture moves (if any). Defaults to None.

        Returns:
            int|float : score of the baord
        """
        if moves == None:
            moves = self.nextMoves(player)
        if len(moves) == 0 or depth == maxDepth:
            score = evaluate(self, maximizer)
            # if there is no escape from losing, maximize number of moves to lose
            if score < 0:
                score += depth
            return score

        bestValue = -self.OO
        if player != maximizer:
            bestValue = self.OO

        # sort moves by the minimum next positions
        moves.sort(key=lambda move: len(move[1]))
        for position in moves:
            x, y = position[0]
            for nx, ny in position[1]:

                canCapture, removed, promoted = self.playMove(x, y, nx, ny)
                played = False

                if canCapture:
                    _, nextCaptures = self.nextPositions(nx, ny)
                    if len(nextCaptures) != 0:
                        played = True
                        nMoves = [((nx, ny), nextCaptures)]
                        if player == maximizer:
                            bestValue = max(
                                bestValue,
                                self.minimax(player, maximizer, depth + 1, alpha, beta, maxDepth, evaluate, nMoves)
                            )
                            alpha = max(alpha, bestValue)
                        else:
                            bestValue = min(
                                bestValue,
                                self.minimax(player, maximizer, depth + 1, alpha, beta, maxDepth, evaluate, nMoves)
                            )
                            beta = min(beta, bestValue)

                if not played:
                    if player == maximizer:
                        bestValue = max(
                            bestValue,
                            self.minimax(1 - player, maximizer, depth + 1, alpha, beta, maxDepth, evaluate)
                        )
                        alpha = max(alpha, bestValue)
                    else:
                        bestValue = min(
                            bestValue,
                            self.minimax(1 - player, maximizer, depth + 1, alpha, beta, maxDepth, evaluate)
                        )
                        beta = min(beta, bestValue)

                self.undoMove(x, y, nx, ny, removed, promoted)

                if beta <= alpha:
                    break
            if beta <= alpha:
                break

        return bestValue

    def minimaxPlay(
        self,
        player: int,
        moves: Moves = None,
        maxDepth: int = 4,
        evaluate: Callable[[int], int] = evaluate2,
        enablePrint: bool = True,
    ) -> Tuple[bool, bool]:
        """play a move using minimax algorithm
            if the player should continue capturing, it will

        Args:
            player (int): the type of the player (WHITE, BLACK)
            moves (Moves, optional): the next capture moves (if any). Defaults to None.
            maxDepth (int, optional): the max depth of the minimax algorithm
                the higher the max depth, the harder the level of th play 
                and the more time the algorithm will take. Defaults to 4.
            enablePrint (bool, optional): if true it prints the game board 
                to stdout after playing the move. Defaults to True.

        Returns:
            continue (bool): false if there is no further plays.  
            reset (bool): true when there is a captured piece, 
                used to reset the counter of the draw condition.
        """

        if moves == None:
            moves = self.nextMoves(player)
        if len(moves) == 0:
            if enablePrint:
                print(("WHITE" if player == self.BLACK else "BLACK") + " Player wins")
            return False, False

        self.stateCounter[self.encodeBoard()] += 1

        random.shuffle(moves)
        bestValue = -self.OO
        bestMove = None

        for position in moves:
            x, y = position[0]
            for nx, ny in position[1]:
                _, removed, promoted = self.playMove(x, y, nx, ny)
                value = self.minimax(1 - player, player, maxDepth=maxDepth, evaluate=evaluate)
                value += 2*self.stateValue(player)  
                self.undoMove(x, y, nx, ny, removed, promoted)
                if value > bestValue:
                    bestValue = value
                    bestMove = (x, y, nx, ny)

        x, y, nx, ny = bestMove
        if enablePrint:
            print(f"Move from ({x}, {y}) to ({nx}, {ny})")
        canCapture, removed, _ = self.playMove(x, y, nx, ny)
        if enablePrint:
            self.printBoard(nx, ny)

        if canCapture:
            _, captures = self.nextPositions(nx, ny)
            if len(captures) != 0:
                self.minimaxPlay(player, [((nx, ny), captures)], maxDepth, evaluate, enablePrint)

        self.stateCounter[self.encodeBoard()] += 1
        reset = removed != 0
        return True, reset
