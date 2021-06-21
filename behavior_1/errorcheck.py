#----------------------------------------------
# ERROR CHECKING
#----------------------------------------------

# helper functions
def yWord(y):
    if y == 0:
        return "top"
    elif y == 1:
        return "middle"
    elif y == 2:
        return "bottom"

def xWord(x):
    if x == 0:
        return "right"
    elif x == 1:
        return "middle"
    elif x == 2:
        return "left"

def transpose(X):
    result = [[X[j][i] for j in range(len(X))] for i in range(len(X[0]))]
    return result

def sPrint(s):
    print(s)

def failPrint(failMsgs, s):
    sPrint(s)
    failMsgs.append(s)
    return failMsgs, True


# initialize variables
oldBoard = [["-","X","O"],["X","O","-"],["-","-","-"]]
newBoard = [["-","X","O"],["X","O","-"],["-","X","-"]]
robotTurn = True
robotCoords = [0,0]
expectedSymbol = "X"

newSymbols = [[None] * len(elem) for elem in oldBoard]
newSymbolCoords = []

failMsgs = []
failed = False

# evaluate board state differences
for y in range(len(oldBoard)):
    for x in range(len(oldBoard[0])):
        if (newBoard[y][x] != oldBoard[y][x]):
            # check for erased symbols
            if newBoard[y][x] == "-":
                failMsgs, failed = failPrint(failMsgs, "Erased symbol at " + yWord(y) + ", " + xWord(x))
            #check for changed symbols
            if oldBoard[y][x] != "-":
                if newBoard[y][x] == "X":
                    failMsgs, failed = failPrint(failMsgs, "O changed to X at " + yWord(y) + ", " + xWord(x))
                elif newBoard[y][x] == "O":
                    failMsgs, failed = failPrint(failMsgs, "X changed to O at " + yWord(y) + ", " + xWord(x))
            else:
                # store new symbols
                newSymbolCoords.append([y,x])
                newSymbols[y][x] = newBoard[y][x]

# check for the proper placement of new symbols
lenNewSymbols = len(newSymbolCoords)
# verify that the robot coord is placed
if robotTurn:
    if newBoard[robotCoords[0]][robotCoords[1]] == "-":
            failMsgs, failed = failPrint(failMsgs, "Expected symbol at " + yWord(robotCoords[0]) + ", " + xWord(robotCoords[1]))
    if lenNewSymbols == 0:
        failMsgs, failed = failPrint(failMsgs, "No new symbols detected")
    else:
        for coord in newSymbolCoords:
            if (robotCoords[0] != coord[0] or robotCoords[1] != coord[1]):
                failMsgs, failed = failPrint(failMsgs, "Extra symbol at " + yWord(coord[0]) + ", " + xWord(coord[1]))
            else:
                if expectedSymbol != newSymbols[coord[0]][coord[1]]:
                    failMsgs, failed = failPrint(failMsgs, "Incorrect symbol at " + yWord(coord[0]) + ", " + xWord(coord[1]))
# choose which new symbol to keep on player turn
else:
    if lenNewSymbols == 0:
        failMsgs, failed = failPrint(failMsgs, "No new symbols detected")
    else:
        if lenNewSymbols > 1:
            for coord in newSymbolCoords:
                failMsgs, failed = failPrint(failMsgs, "Extra symbol at " + yWord(coord[0]) + ", " + xWord(coord[1]))
            failMsgs, failed = failPrint(failMsgs, "Please keep only one new symbol")
        else:
            newCoord = newSymbolCoords[0]
            if expectedSymbol != newSymbols[newCoord[0]][newCoord[1]]:
                failMsgs, failed = failPrint(failMsgs, "Incorrect symbol at " + yWord(newCoord[0]) + ", " + xWord(newCoord[1]))

sPrint(failMsgs)
sPrint("Failed: " + str(failed))