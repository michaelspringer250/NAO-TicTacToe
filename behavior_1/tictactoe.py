#import sys
#import ALProxy
import numpy as np
import copy
import random

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
# None = tie, -1 = unfinished, X = X wins, O = O wins
def evaluate(board):
    winner = None
      
    for player in ["X", "O"]:
        if (row_win(board, player) or
            col_win(board,player) or 
            diag_win(board,player)):
                
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

def scoreResult(result, player):
  if result == None:
    return 0
  else:
    if result == player:
      return 1
    else:
      return -1

# Evaluates the next move to make
def branch(board, player, playedCoord):
    result = evaluate(board)

    if result == -1:
        #continue branching
        nextPlayer = None
        if player == "O":
            nextPlayer = "X"
        else:
            nextPlayer = "O"

        positions = possibilities(board)
        nextBoard = None
        bestOptions = []
        largest = None
        winFound = False
        for pos in positions:
            nextBoard = copy.deepcopy(board)
            nextBoard[pos[0]][pos[1]] = player
            evaluation = evaluate(nextBoard)
            if evaluation == player:
                winFound = True
                bestOptions.append((evaluation, pos))
        if winFound == False:
            for pos in positions:
                nextBoard = copy.deepcopy(board)
                nextBoard[pos[0]][pos[1]] = player
                nextResult, _ = branch(nextBoard, nextPlayer, pos)
                score = scoreResult(nextResult, player)
                #choose the best branch to return
                if largest == None or largest < score:
                    largest = score
                    bestOptions = [(nextResult, pos)]
                elif largest == score:
                    bestOptions.append((nextResult, pos))

        idx = random.randint(0,len(bestOptions)-1)
        bestResult = bestOptions[idx][0]
        bestCoord = bestOptions[idx][1]
        return bestResult, bestCoord
    else:
        return result, playedCoord

board = [
["-","-","-"],
["-","-","-"],
["-","-","X"]]

player = "O"

result, playedCoord = branch(board, player, None)
print(result)
print(playedCoord)