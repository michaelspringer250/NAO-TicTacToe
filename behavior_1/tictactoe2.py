#from naoqi import ALProxy
import enum
import numpy as np
import copy
import random

class PType(enum.Enum):
   P1 = 1
   P2 = 2

class Modifiers(enum.Enum):
   Wild = 1
   Reverse = 2

def yWord(y):
    if y == 0:
        return "top"
    elif y == 1:
        return "middle"
    elif y == 2:
        return "bottom"

def xWord(x):
    if x == 0:
        return "left"
    elif x == 1:
        return "middle"
    elif x == 2:
        return "right"


# Checks whether the player has three
# of their marks in a horizontal row
def row_win(board, player):
    length = len(board)
    for x in range(length):
        win = True

        for y in range(length):
            if board[x][y] != player:
                win = False
                continue

        if win == True:
            return(win)
    return(win)

# Checks whether the player has three
# of their marks in a vertical row
def col_win(board, player):
    length = len(board)
    for x in range(length):
        win = True

        for y in range(length):
            if board[y][x] != player:
                win = False
                continue

        if win == True:
            return(win)
    return(win)

# Checks whether the player has three
# of their marks in a diagonal row
def diag_win(board, player):
    win = True
    y = 0
    length = len(board)
    for x in range(length):
        if board[x][x] != player:
            win = False
    if win:
        return win
    win = True
    if win:
        for x in range(length):
            y = length - 1 - x
            if board[x][y] != player:
                win = False
    return win

# Evaluates whether there is
# a winner or a tie
# player is the one who made the most recent move
# None = tie, -1 = unfinished, PType.P1 = P1 wins, PType.P2 = P2 wins
def evaluate(modifiers, board, player):
    winner = None
    length = len(board)

    for symbol in ["X", "O"]:
        if (row_win(board, symbol) or
            col_win(board,symbol) or
            diag_win(board,symbol)):

            winner = player

    if winner == None:
        for x in range(length):
            if winner == -1:
                break
            for y in range(length):
                if board[x][y] == "-":
                    winner = -1
                    break

    if Modifiers.Reverse in modifiers and winner != None and winner != -1:
        return PType.P1 if winner == PType.P2 else PType.P2
    else:
        return winner

# Check for empty places on board
def possibilities(board):
    l = []
    length = len(board)

    for i in range(length):
        for j in range(length):

            if board[i][j] == "-":
                l.append((i, j))
    return(l)

# Score a result
def scoreResult(result, player, depth):
    depthInfluence = depth / 50.0
    if result == None or result == -1:
        return 0
    if result == player:
        return 1 - depthInfluence
    else:
        return -1 + depthInfluence

# Evaluates the next move to make
# "playedSymbol" parameter only used with wild modifier
# "symbol" paramter only used without wild modifier
def branch(depth, modifiers, board, player, symbol, playedCoord, playedSymbol):
    # evaulate the result assuming the previous player made the last move
    result = evaluate(modifiers, board, PType.P1 if player == PType.P2 else PType.P2)

    if result == -1:
        #continue branching
        nextPlayer = None
        if player == PType.P1:
            nextPlayer = PType.P2
        else:
            nextPlayer = PType.P1

        nextSymbol = None
        if symbol == "X":
            nextSymbol = "O"
        else:
            nextSymbol = "X"

        positions = possibilities(board)
        nextBoard = None
        bestOptions = []
        largest = None
        winFound = False
        for pos in list(positions):
            nextBoard = copy.deepcopy(board)
            # search both X and O placements if we're playing wild
            if Modifiers.Wild in modifiers:
                for sym in ["X", "O"]:
                    nextBoard[pos[0]][pos[1]] = sym
                    evaluation = evaluate(modifiers, nextBoard, player)
                    score = scoreResult(evaluation, player, depth + 1)
                    if score > 0:
                        winFound = True
                        bestOptions.append((player, pos, sym, depth + 1))
            # otherwise just use the next symbol
            else:
                nextBoard[pos[0]][pos[1]] = symbol
                evaluation = evaluate(modifiers, nextBoard, player)
                score = scoreResult(evaluation, player, depth + 1)
                if score > 0:
                    winFound = True
                    bestOptions.append((player, pos, symbol, depth + 1))
        if winFound == False:
            for pos in positions:
                nextBoard = copy.deepcopy(board)
                # search both X and O placements if we're playing wild
                if Modifiers.Wild in modifiers:
                    for sym in ["X", "O"]:
                        nextBoard[pos[0]][pos[1]] = sym
                        nextResult, _, _, resultDepth = branch(depth + 1, modifiers, nextBoard, nextPlayer, nextSymbol, pos, sym)
                        score = scoreResult(nextResult, player, resultDepth)
                        # choose the best branch to return
                        if largest == None or largest < score:
                            largest = score
                            bestOptions = [(nextResult, pos, sym, resultDepth)]
                        elif largest == score:
                            bestOptions.append((nextResult, pos, sym, resultDepth))
                # otherwise just use the next symbol
                else:
                    nextBoard[pos[0]][pos[1]] = symbol
                    nextResult, _, _, resultDepth = branch(depth + 1, modifiers, nextBoard, nextPlayer, nextSymbol, pos, symbol)
                    score = scoreResult(nextResult, player, resultDepth)
                    # choose the best branch to return
                    if largest == None or largest < score:
                        largest = score
                        bestOptions = [(nextResult, pos, symbol, resultDepth)]
                    elif largest == score:
                        bestOptions.append((nextResult, pos, symbol, resultDepth))

        idx = random.randint(0,len(bestOptions)-1)
        bestResult = bestOptions[idx][0]
        bestCoord = bestOptions[idx][1]
        bestSymbol = bestOptions[idx][2]
        bestDepth = bestOptions[idx][3]
        
        return bestResult, bestCoord, bestSymbol, bestDepth
    else:
        return result, playedCoord, playedSymbol, depth


#board = self.mem.getData("board")
board = [["X","O","X"],
        ["O","X","O"],
        ["-","O","X"]]
#player = "O" if self.mem.getData("marker") == "X" else "X"
result, playedCoord, playedSymbol, resultDepth = branch(0, [Modifiers.Wild], board, PType.P1, "X", None, None)
print(result, playedCoord, playedSymbol, resultDepth)
#self.mem.insertData("robotCoords", playedCoord)
#self.tts.say(yWord(playedCoord[0]) + ", " + xWord(playedCoord[1]))
#self.onStopped(playedCoord)
