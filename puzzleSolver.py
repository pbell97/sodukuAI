import math


class PuzzleSolver():
    def __init__(self):
        None

    def convertSubGridsTo2xList(self, puzzle):
        # puzzle[majorRow][majorColumn][subGridRow][subGridColumn]
        # newPuzzle[row][column] ----> Non-zero indexed

        # Makes 9x9 grid with unused first row/col
        newPuzzle = []
        for i in range(10):
            newPuzzle.append([])
            for j in range(10):
                newPuzzle[i].append('blank')

        # Gets each item from old format and converts to new row, col
        for subGridRow in range(3):
            for subGridCol in range(3):
                for gridRow in range(3):
                    for gridCol in range(3):
                        item = puzzle[subGridRow][subGridCol][gridRow][gridCol]
                        row = subGridRow*3 + gridRow + 1
                        col = subGridCol*3 + gridCol + 1
                        newPuzzle[row][col] = item

        return newPuzzle

    # True if row is valid, false if duplicates

    def checkRow(self, puzzle, row):
        foundNumbers = []
        for col in range(1, 10):
            num = puzzle[row][col]
            if num == 'blank':
                continue
            elif num in foundNumbers:
                return False
            else:
                foundNumbers.append(num)
        return True

    def checkColumn(self, puzzle, col):
        foundNumbers = []
        for row in range(1, 10):
            num = puzzle[row][col]
            if num == 'blank':
                continue
            elif num in foundNumbers:
                return False
            else:
                foundNumbers.append(num)
        return True

    # Checks validity of subgrid given a specific cell

    def checkSubGrid(self, puzzle, row, col):
        startingRow = math.floor(row/3)*3 + 1
        startingCol = math.floor(col/3)*3 + 1

        foundNumbers = []

        for rowInc in range(0, 3):
            for colInc in range(0, 3):
                print("Row: " + str(startingRow + rowInc) +
                      " Col: " + str(startingCol + colInc))
                num = puzzle[startingRow + rowInc][startingCol + colInc]
                if num == 'blank':
                    continue
                elif num in foundNumbers:
                    return False
                else:
                    foundNumbers.append(num)
        return True

    def checkWholePuzzle(self, puzzle):
        # Checks all rows/columns
        for i in range(1, 10):
            if not self.checkRow(puzzle, i):
                return False
            if not self.checkColumn(puzzle, i):
                return False

        # Checks all sub grids
        startingCell = [2, 2]
        for i in range(0, 7, 3):
            for j in range(0, 7, 3):
                print(startingCell[0] + i, startingCell[1] + j)
                if not self.checkSubGrid(puzzle, startingCell[0] + i, startingCell[1] + j):
                    return False

        return True
