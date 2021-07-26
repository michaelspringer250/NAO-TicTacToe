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
    for x in range(len(board)):
        win = True

        for y in range(len(board)):
            if board[x][y] != player:
                win = False
                continue

        if win == True:
            return(win)
    return(win)

# Checks whether the player has three
# of their marks in a vertical row
def col_win(board, player):
    for x in range(len(board)):
        win = True

        for y in range(len(board)):
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
    for x in range(len(board)):
        if board[x][x] != player:
            win = False
    if win:
        return win
    win = True
    if win:
        for x in range(len(board)):
            y = len(board) - 1 - x
            if board[x][y] != player:
                win = False
    return win

# Evaluates whether there is
# a winner or a tie
# None = tie, -1 = unfinished, PType.P1 = P1 wins, PType.P2 = P2 wins
def evaluate(board, player):
    winner = None

    for symbol in ["X", "O"]:
        if (row_win(board, symbol) or
            col_win(board,symbol) or
            diag_win(board,symbol)):

            winner = player

    if winner == None:
        for x in range(len(board)):
            if winner == -1:
                break
            for y in range(len(board)):
                if board[x][y] == "-":
                    winner = -1
                    break

    return winner

# Check for empty places on board
def possibilities(board):
    l = []

    for i in range(len(board)):
        for j in range(len(board)):

            if board[i][j] == "-":
                l.append((i, j))
    return(l)

def scoreResult(modifiers, result, player):
  if result == None:
    return 0
  else:
    if Modifiers.Reverse in modifiers:
        if result == player:
            return -1
        else:
            return 1
    else:
        if result == player:
            return 1
        else:
            return -1

# Evaluates the next move to make
# "playedSymbol" parameter only used with wild modifier
# "symbol" paramter only used without wild modifier
def branch(modifiers, board, player, symbol, playedCoord, playedSymbol):
    result = evaluate(board, player)

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
        for pos in positions:
            nextBoard = copy.deepcopy(board)
            # search both X and O placements if we're playing wild
            if Modifiers.Wild in modifiers:
                for sym in ["X", "O"]:
                    nextBoard[pos[0]][pos[1]] = sym
                    evaluation = evaluate(nextBoard, player)
                    if evaluation == player:
                        winFound = True
                        bestOptions.append((player, pos, sym))
            # otherwise just use the next symbol
            else:
                nextBoard[pos[0]][pos[1]] = symbol
                evaluation = evaluate(nextBoard, player)
                if evaluation == player:
                    winFound = True
                    bestOptions.append((player, pos))
        if winFound == False:
            for pos in positions:
                nextBoard = copy.deepcopy(board)
                # search both X and O placements if we're playing wild
                if Modifiers.Wild in modifiers:
                    for sym in ["X", "O"]:
                        nextBoard[pos[0]][pos[1]] = sym
                        nextResult, _, _ = branch(modifiers, nextBoard, nextPlayer, nextSymbol, pos, sym)
                        score = scoreResult(modifiers, nextResult, player)
                        # choose the best branch to return
                        if largest == None or largest < score:
                            largest = score
                            bestOptions = [(nextResult, pos, sym)]
                        elif largest == score:
                            bestOptions.append((nextResult, pos, sym))
                # otherwise just use the next symbol
                else:
                    nextBoard[pos[0]][pos[1]] = symbol
                    nextResult, _, _ = branch(modifiers, nextBoard, nextPlayer, nextSymbol, pos, symbol)
                    score = scoreResult(modifiers, nextResult, player)
                    # choose the best branch to return
                    if largest == None or largest < score:
                        largest = score
                        bestOptions = [(nextResult, pos)]
                    elif largest == score:
                        bestOptions.append((nextResult, pos))

        idx = random.randint(0,len(bestOptions)-1)
        bestResult = bestOptions[idx][0]
        bestCoord = bestOptions[idx][1]
        if Modifiers.Wild in modifiers:
            bestSymbol = bestOptions[idx][2]
            return bestResult, bestCoord, bestSymbol
        else:
            return bestResult, bestCoord
    else:
        if Modifiers.Wild in modifiers:
            return result, playedCoord, playedSymbol
        else:
            return result, playedCoord


#board = self.mem.getData("board")
board = [["-","O","-"],
        ["O","X","O"],
        ["O","O","O"]]
#player = "O" if self.mem.getData("marker") == "X" else "X"
player = PType.P1
result, playedCoord, playedSymbol = branch([Modifiers.Wild], board, player, None, None, None)
print(result, playedCoord, playedSymbol)
#self.mem.insertData("robotCoords", playedCoord)
#self.tts.say(yWord(playedCoord[0]) + ", " + xWord(playedCoord[1]))
#self.onStopped(playedCoord)
