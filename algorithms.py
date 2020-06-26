from typeRotation import *
from typeDirection import *
from typeAngle import *
from typeCell import *
from typeThick import *
import numpy as np
import copy

def findDir(rotationType, angleType):
    """returns the direction from our perspective (primarily for the arrow)"""

    if(rotationType == RotationType.left):
        if(angleType == AngleType.lacute):
            return DirectionType.lowerright 
        elif(angleType == AngleType.racute):
            return DirectionType.upperright
        elif(angleType == AngleType.lright):
            return DirectionType.down
        elif(angleType == AngleType.rright):
            return DirectionType.up
        elif(angleType == AngleType.lobtuse):
            return DirectionType.lowerleft
        elif(angleType == AngleType.robtuse):
            return DirectionType.upperleft
        elif(angleType == AngleType.straight):
            return DirectionType.left
        else:
            raise Exception("uh oh, either angleType is NA or arrow is somehow going in a straight line :O")
    
    elif(rotationType == RotationType.right): 
        if(angleType == AngleType.lacute):
            return DirectionType.upperleft
        elif(angleType == AngleType.racute):
            return DirectionType.lowerleft
        elif(angleType == AngleType.lright):
            return DirectionType.up
        elif(angleType == AngleType.rright):
            return DirectionType.down
        elif(angleType == AngleType.lobtuse):
            return DirectionType.upperright
        elif(angleType == AngleType.robtuse):
            return DirectionType.upperleft
        elif(angleType == AngleType.straight):
            return DirectionType.right
        else:
            raise Exception("uh oh, either angleType is NA or arrow is somehow going in a straight line :O")

    elif(rotationType == RotationType.up): 
        if(angleType == AngleType.lacute):
            return DirectionType.lowerleft
        elif(angleType == AngleType.racute):
            return DirectionType.lowerright
        elif(angleType == AngleType.lright):
            return DirectionType.left
        elif(angleType == AngleType.rright):
            return DirectionType.right
        elif(angleType == AngleType.lobtuse):
            return DirectionType.upperleft
        elif(angleType == AngleType.robtuse):
            return DirectionType.upperright
        elif(angleType == AngleType.straight):
            return DirectionType.up
        else:
            raise Exception("uh oh, either angleType is NA or arrow is somehow going in a straight line :O")

    elif(rotationType == RotationType.down):
        if(angleType == AngleType.lacute):
            return DirectionType.upperright
        elif(angleType == AngleType.racute):
            return DirectionType.upperleft
        elif(angleType == AngleType.lright):
            return DirectionType.right
        elif(angleType == AngleType.rright):
            return DirectionType.left
        elif(angleType == AngleType.lobtuse):
            return DirectionType.lowerright
        elif(angleType == AngleType.robtuse):
            return DirectionType.lowerleft
        elif(angleType == AngleType.straight):
            return DirectionType.down
        else:
            raise Exception("uh oh, either angleType is NA or arrow is somehow going in a straight line :O")


def formatMatrix(matrix):  
    string = ""
    colLength = len(matrix)
    rowLength = len(matrix[0])
    for y in range(colLength):
        for x in range(rowLength):
            string += str(matrix[y][x]) + "\t"
        string += "\n\n\n"
    return string

def flatten(l):
    return [item for sublist in l for item in sublist]


def rotateInitialBoard(initialboard):
    initialboard = copy.deepcopy(initialboard)
    colLength = len(initialboard)
    rowLength = len(initialboard[0])
    for y in range(colLength):
        for x in range(rowLength):
            cellInfo = initialboard[y][x]
            if cellInfo[3] != RotationType.na.value:
                print(initialboard[y][x])
                initialboard[y][x] = cellInfo[:3] + str((int(cellInfo[3]) + 6) % 8) + cellInfo[4:] #rotate 90 degrees
                print(initialboard[y][x])
    return rotateMatrix(initialboard)

def rotateMatrix(matrix):
    newRowLength = len(matrix)
    newColLength = len(matrix[0])
    newMatrix = []
    for y in range(newColLength):
        row = []
        for x in range(newRowLength):
            row.append(copy.deepcopy(matrix[x][newColLength-1-y]))
        newMatrix.append(row)
    return newMatrix

def rotateGopherCell(gopherCell, originalrowlength):
    oldx, oldy, oldrotation, state = gopherCell
    newx = oldy
    newy = originalrowlength - 1 - oldx
    newrotation = (oldrotation + 6) % 8
    return (newx, newy, newrotation, state)

def rotateSimulation(initialboard, activeCells, gopherCells):
    newac = []
    newgc = []
    originalrowlength = len(initialboard[0])
    for step in range(len(activeCells)):
        newac.append(rotateMatrix(activeCells[step]))
        newgc.append(rotateGopherCell(gopherCells[step], originalrowlength))
    newib = rotateInitialBoard(initialboard)
    return newib, newac, newgc

def addTrapToTerrain(terrain, start_x, start_y, trapboard):
        """adds a 'miniboard' to self's board with the top left corner at the indicated position"""
        rowLength = len(trapboard[0])
        colLength = len(trapboard)
        trLength = len(terrain[0])
        tcLength = len(terrain)
        if start_x + rowLength <= trLength:
            if start_y + colLength <= tcLength:
                for x in range(rowLength):
                    for y in range(colLength):
                        terrain[start_y + y][start_x + x] = trapboard[y][x]
                return terrain
        raise Exception("This board does not fit")

## still need to check in the case that the connected wire cells are the same thicktype
def checkBrokenTrap(trap, wire):
    """
    Helper function for gopherProbEnter.
    Covers the base cases for a broken trap--traps that pose no danger to the gopher.
    Returns a probability of 0.9?? since the gopher will not be hurt by entering
    """
    allCells = flatten(trap.board[y][x])
    wireCells = []
    arrowCells = []
    arrowLoc = [] #will be list of lists
    doorLoc = []
    wireThickTypes = [0,0,0]
    arrowThickTypes = [0,0,0]
    # [skinny, normal, wide]

    for cell in allCells: # flattens board into 1d  array
        if cell.cellType == CellType.wire:
            wireCells.append(cell)
        elif cell.cellType == CellType.arrow:
            arrowCells.append(cell)
            arrowLoc.append(cell)
        elif cell.cellType == CellType.door:
            doorLocation.append(cell)

    for cell in wireCells:
        wireThickTypes[cell.thickType.value] += 1

    for cell in arrowCells:
        arrowThickTypes[cell.thickType.value] += 1

    ## BROKEN TRAP CASES
    ## !!Need to check if correct thicktypes are connected and return high probability if they are

    only = lambda ind, typelist: sum([typelist[i] > 0 for i in range(len(typelist)) if i != ind])==0

    # Case: when all arrows/wires are of uniform thickness
    if wireCells.len() and arrowCells.len() == 0:
        if arrowCells.len() == 0:
            print("No danger and highest probability")
            return 0.9
        else:
            if door.Loc : #connected to gate, placed filler
                if arrowThickTypes == 0: #not zero!!
                    return 0.7 # or a probability that reflects the 
            else:
                return 0.9 # or 1?
    
    

def gopherProbEnter1(trap):
    """
    This returns the probability that the gopher will enter for working traps.
    Working traps are traps that are able to hurt the gopher
    """
    ## WORKING TRAP CASES
    ## Case: only arrows with no wires, but arrows are connected to the gate so they still fire

    if (wireThickTypes[2] and arrowThickTypes[2] > 0) and all(i is 0 for i in wireThickTypes[:2]) and all(j is 0 for j in arrowThickTypes[:2]):
        print("All wide thickness. very thicc. Highest danger and low probability of entering")
        return 0.1
    if (wireThickTypes[1] and arrowThickTypes[1] > 0) and all(i is 0 for i in wireThickTypes.remove(wireThickTypes[1])) and only(1, wireThickTypes):
        print("All normal thickness. Medium danger and medium probability of entering")
        return 0.5
    if (wireThickTypes[0] and arrowThickTypes[0] > 0) and all(i is 0 for i in wireThickTypes[0:]) and all(j is 0 for j in wireThickTypes[0:]):
        print("All skinny thickness. low danger and high probability of entering")
        return 0.8

    ### CASE: when >1 arrow AND not uniform thickness

def gopherProbEnter2(trap):
    thickTypes = [0,0,0]
    hasArrow = False
    for cell in flatten(trap.board):
        if cell.thickType != ThickType.na:
            thickTypes[cell.thickType.value] += 1
            if cell.cellType == CellType.arrow:
                hasArrow = True
    if hasArrow == False:
        return 1.0
    valuelist = []
    for value in range(3):
        valuelist += [value] * thickTypes[value]
    std = np.std(valuelist)
    mean = np.mean(valuelist)

    cohesion = 1 - std #for 3 values, maximum standard deviation is 1, which is least threat
    damage_potential = mean / 3 #maximum mean is 3 (biggest threat)
    threat = (0.7 * cohesion) + (0.3 * damage_potential) #cohesion is more important
    probEnter = 1 - threat
    return probEnter