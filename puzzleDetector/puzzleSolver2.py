import cv2
import math
import time
# Thought: Run a general puzzle check on a new inputted puzzle to see if there are any errors

puzzle = [['8', 'blank', 'blank', 'blank', 'blank', 'blank', 'blank', 'blank', 'blank'],
          ['blank', 'blank', 'blank', 'blank', 'blank', '3', 'blank', '8', '5'],
          ['blank', 'blank', '1', 'blank', '2',
              'blank', 'blank', 'blank', 'blank'],
          ['blank', 'blank', 'blank', '5', 'blank', '7', 'blank', 'blank', 'blank'],
          ['blank', 'blank', '4', 'blank', 'blank', 'blank', '1', 'blank', 'blank'],
          ['blank', '9', 'blank', 'blank', 'blank',
              'blank', 'blank', 'blank', 'blank'],
          ['5', 'blank', 'blank', 'blank', 'blank', 'blank', 'blank', '7', '3'],
          ['blank', 'blank', '2', 'blank', '1',
              'blank', 'blank', 'blank', 'blank'],
          ['blank', 'blank', 'blank', 'blank', '4', 'blank', 'blank', 'blank', '9']]


puzzle = [['5', '3', 'blank', 'blank', '7', 'blank', 'blank', 'blank', 'blank'],
          ['6', 'blank', 'blank', '1', '9', '5', 'blank', 'blank', 'blank'],
          ['blank', '9', '8', 'blank', 'blank', 'blank', 'blank', '6', 'blank'],
          ['8', 'blank', 'blank', 'blank', '6', 'blank', 'blank', 'blank', '3'],
          ['4', 'blank', 'blank', '8', 'blank', '3', 'blank', 'blank', '1'],
          ['7', 'blank', 'blank', 'blank', '2', 'blank', 'blank', 'blank', '6'],
          ['blank', '6', 'blank', 'blank', 'blank', 'blank', '2', '8', 'blank'],
          ['blank', 'blank', 'blank', '4', '1', '9', 'blank', 'blank', '5'],
          ['blank', 'blank', 'blank', 'blank', '8', 'blank', 'blank', '7', '9']]


def rowIsValid(puzzle, rowNumber):
    numbers = puzzle[rowNumber]
    existingNumbers = []
    for number in numbers:
        if number in existingNumbers and number != 'blank':
            return False
        else:
            existingNumbers.append(number)
    return True


def getNumbersInRow(puzzle, rowNumber):
    numbers = puzzle[rowNumber]
    existingNumbers = []
    for number in numbers:
        if number not in existingNumbers and number != 'blank':
            existingNumbers.append(number)
    return existingNumbers


def columnIsValid(puzzle, colNumber):
    existingNumbers = []
    for i in range(9):
        number = puzzle[i][colNumber]
        if number in existingNumbers and number != 'blank':
            return False
        else:
            existingNumbers.append(number)
    return True


def getNumbersInColumn(puzzle, colNumber):
    existingNumbers = []
    for i in range(9):
        number = puzzle[i][colNumber]
        if number not in existingNumbers and number != 'blank':
            existingNumbers.append(number)
    return existingNumbers


def groupIsValid(puzzle, rowNumber, colNumber):
    existingNumbers = []
    firstRowNum = math.floor(rowNumber/3)*3
    firstColNum = math.floor(colNumber/3)*3
    for i in range(3):
        for j in range(3):
            number = puzzle[firstRowNum+i][firstColNum+j]
            if number in existingNumbers and number != 'blank':
                return False
            else:
                existingNumbers.append(number)
    return True


def getNumbersInGroup(puzzle, rowNumber, colNumber):
    existingNumbers = []
    firstRowNum = math.floor(rowNumber/3)*3
    firstColNum = math.floor(colNumber/3)*3
    for i in range(3):
        for j in range(3):
            number = puzzle[firstRowNum+i][firstColNum+j]
            if number not in existingNumbers and number != 'blank':
                existingNumbers.append(number)

    return existingNumbers


def getPossibleNumbers(puzzle, rowNumber, colNumber):
    possibleValues = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    existingNumbers = getNumbersInRow(puzzle, rowNumber) + getNumbersInColumn(
        puzzle, colNumber) + getNumbersInGroup(puzzle, rowNumber, colNumber)
    for number in existingNumbers:
        if number in possibleValues:
            possibleValues.remove(number)

    return possibleValues


def puzzleIsValid(puzzle):
    for i in range(9):
        if not rowIsValid(puzzle, i):
            return False
        if not columnIsValid(puzzle, i):
            return False
    for i in range(3):
        for j in range(3):
            if not groupIsValid(puzzle, i*3, j*3):
                return False
    return True


def cellisValid(puzzle, rowNumber, colNumber):
    return rowIsValid(puzzle, rowNumber) and columnIsValid(puzzle, colNumber) and groupIsValid(puzzle, rowNumber, colNumber)


def getNextCell(rowNumber, columnNumber, method="down"):
    if str.lower(method) == "down":
        if rowNumber < 8:
            return (rowNumber + 1, columnNumber)
        elif rowNumber == 8 and columnNumber != 8:
            return (0, columnNumber + 1)
        else:
            return None


def solve(puzzle):
    cell = {
        'row': 0,
        'column': 0,
        'value': puzzle[0][0],
        'isFixed': True if puzzle[0][0] != 'blank' else False
    }

    cellSolve(puzzle, cell)


def cellSolve(puzzle, cell):

    # DO check if its a fixedCell and skip is so
    # if str(time.time()).split('.')[0][9] == "0":
    #     print("At ", cell)
    if cell['value'] == 'blank':
        possibleValues = getPossibleNumbers(
            puzzle, cell['row'], cell['column'])

        if len(possibleValues) == 0:
            return False

        # Prune the tree - get rid of known duplicates from possible values
        # Forward checking

        for possibleValue in possibleValues:
            if cell['row'] == 0 and cell['column'] == 0:
                print("At 0,0")
            cell['value'] = possibleValue
            puzzle[cell['row']][cell['column']] = cell['value']
            isValid = cellisValid(puzzle, cell['row'], cell['column'])
            if not isValid and possibleValue != possibleValues[-1]:
                puzzle[cell['row']][cell['column']] = 'blank'
                continue
            elif not isValid and possibleValue == possibleValues[-1]:
                puzzle[cell['row']][cell['column']] = 'blank'
                # Need to backtrack
                return False
            elif isValid:
                # Call this sequence on the next cell
                nextPosition = getNextCell(cell['row'], cell['column'], "down")
                if nextPosition == None:
                    print("SOLVED")
                    for i in range(9):
                        print(puzzle[i])
                    return puzzle
                else:
                    newCell = {
                        'row': nextPosition[0],
                        'column': nextPosition[1],
                        'value': puzzle[nextPosition[0]][nextPosition[1]],
                        'isFixed': True if puzzle[nextPosition[0]][nextPosition[1]] != 'blank' else False
                    }
                    result = cellSolve(puzzle, newCell)

                    # If nextCell failed, we move on to next possible value for this cell
                    if result == False and possibleValue != possibleValues[-1]:
                        puzzle[cell['row']][cell['column']] = 'blank'
                        continue
                    # If cell is on last possibleValue, then continueing would be bad, so we return false
                    elif result == False and possibleValue == possibleValues[-1]:
                        puzzle[cell['row']][cell['column']] = 'blank'
                        return False
                    # If nextCell doesn't fail, we return the result
                    else:
                        if cell['row'] == 0 and cell['column'] == 0:
                            print(puzzle)
                        return result
    else:
        nextPosition = getNextCell(cell['row'], cell['column'], "down")
        if nextPosition == None:
            print("SOLVED")
            for i in range(9):
                print(puzzle[i])
            return puzzle
        else:
            newCell = {
                'row': nextPosition[0],
                'column': nextPosition[1],
                'value': puzzle[nextPosition[0]][nextPosition[1]],
                'isFixed': True if puzzle[nextPosition[0]][nextPosition[1]] != 'blank' else False
            }
            result = cellSolve(puzzle, newCell)
            if result == False:
                return False
            else:
                return result

# Need to track nodes expanded


start = time.time()
r = solve(puzzle)
print(r)
print(time.time()-start)

# Error when it the previous number is at 9 and it backtracks...


# In paper: Discuss time complexity (hard to quantify since board is always same side), would be exponential tho in number of boards?
