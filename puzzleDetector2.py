import cv2
import imutils
import numpy as np
import time
from matplotlib import pyplot as plt
from keras.models import load_model
import PIL
from PIL import Image, ImageDraw, ImageFont, ImageOps
import os
import random
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
import pathlib
import copy
import math
import random
from digitClassifier import DigitClassifierNN


class Puzzle:
    def __init__(self, imagePath):
        self.imagePath = imagePath
        self.originalImage = self.loadImage(self.imagePath)
        self.originalImage = self.cropToGrid()
        self.cells = None
        self.numberedCells = None

    def loadImage(self, path):
        return cv2.imread(path)

    def findGridColor(self):
        threshhold = 0.4
        for i in range(self.originalImage.shape[0]):
            color = self.originalImage[i][i]
            if color[0] < 200 and color[1] < 200 and color[2] < 200:
                blackLower = (
                    color[0]-color[0]*threshhold, color[1]-color[1]*threshhold, color[2]-color[2]*threshhold)
                blackUpper = (
                    color[0]+color[0]*threshhold, color[1]+color[1]*threshhold, color[2]+color[2]*threshhold)
                break
        return blackLower, blackUpper

    def cropToGrid(self):
        blackLower, blackUpper = self.findGridColor()
        mask = cv2.inRange(self.originalImage, blackLower, blackUpper)
        # TODO: Debug show mask

        cnts = cv2.findContours(
            mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnt = max(cnts, key=cv2.contourArea)
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        # Assign coordinates of rectangle
        topLeftCornerX = box[1][0]
        topLeftCornerY = box[1][1]
        bottomRightCornerX = box[3][0]
        bottomRightCornerY = box[3][1]
        gridCorners = (topLeftCornerX, topLeftCornerY,
                       bottomRightCornerX, bottomRightCornerY)
        croppedImageWithGrid = self.originalImage[topLeftCornerY:
                                                  bottomRightCornerY, topLeftCornerX:bottomRightCornerX]
        return croppedImageWithGrid

    def showImage(self, image, title):
        cv2.imshow(title, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        cv2.waitKey(1)

    def pixelIsBlack(self, pixel):
        blackValue = 200
        if pixel[0] < blackValue and pixel[1] < blackValue and pixel[2] < blackValue:
            return True
        else:
            return False

    # TODO: Should consider what happens if image doesn't have a white border.
    # May want to crop to grid first to avoid accidentally getting on a line
    def findLinesOld(self):
        # Image goes
        # originalImage[height, width]
        #
        # (0,0) --------> originalImage[0][100]
        # |
        # |
        # |
        # |
        # originalImage[100][0]

        # Height, width, channels
        shape = self.originalImage.shape
        # shape = (shape[0] - 1, shape[1] - 1)
        # Gets x coordinates of 1/6, 3/6, 5/6 of image to navigate downward
        xPoints = [int(shape[1]/6), int(shape[1]/6)*3, int(shape[1]/6)*5]
        yPoints = [int(shape[0]/6), int(shape[0]/6)*3, int(shape[0]/6)*5]

        horizontalLines = []
        i = 0
        while i < shape[0]:
            point1 = self.originalImage[i, xPoints[0]]
            point2 = self.originalImage[i, xPoints[1]]
            point3 = self.originalImage[i, xPoints[2]]
            lineStart = None
            if self.pixelIsBlack(point1) and self.pixelIsBlack(point2) and self.pixelIsBlack(point3):
                lineStart = i
                while self.pixelIsBlack(point1) and self.pixelIsBlack(point2) and self.pixelIsBlack(point3) and i < shape[0]:
                    i = i + 1

                    point1 = self.originalImage[i, xPoints[0]]
                    point2 = self.originalImage[i, xPoints[1]]
                    point3 = self.originalImage[i, xPoints[2]]

                if lineStart:
                    horizontalLines.append((lineStart, i-1))
            i = i+1

        verticalLines = []
        i = 0
        while i < shape[1]:
            point1 = self.originalImage[yPoints[0], i]
            point2 = self.originalImage[yPoints[1], i]
            point3 = self.originalImage[yPoints[2], i]
            lineStart = None
            if self.pixelIsBlack(point1) and self.pixelIsBlack(point2) and self.pixelIsBlack(point3):
                lineStart = i
                while self.pixelIsBlack(point1) and self.pixelIsBlack(point2) and self.pixelIsBlack(point3) and i < shape[1]:
                    i = i + 1

                    point1 = self.originalImage[yPoints[0], i]
                    point2 = self.originalImage[yPoints[1], i]
                    point3 = self.originalImage[yPoints[2], i]
            if lineStart:
                verticalLines.append((lineStart, i-1))

            i = i+1

        return {"horizontalLines": horizontalLines, "verticalLines": verticalLines}

    def findLines(self):
        # Image goes
        # originalImage[height, width]
        #
        # (0,0) --------> originalImage[0][100]
        # |
        # |
        # |
        # |
        # originalImage[100][0]

        # Height, width, channels
        shape = self.originalImage.shape
        # shape = (shape[0] - 1, shape[1] - 1)
        # Gets x coordinates of 1/6, 3/6, 5/6 of image to navigate downward
        # xPoints = [int(shape[1]/6), int(shape[1]/6)*3, int(shape[1]/6)*5]
        # yPoints = [int(shape[0]/6), int(shape[0]/6)*3, int(shape[0]/6)*5]
        xPoints = []
        yPoints = []

        numOfLines = 8
        for i in range(numOfLines):
            xPoints.append(random.randint(0, shape[1]))
            yPoints.append(random.randint(0, shape[1]))

        horizontalLines = []
        i = 0
        while i < shape[0]:
            point1 = self.originalImage[i, xPoints[0]]
            point2 = self.originalImage[i, xPoints[1]]
            point3 = self.originalImage[i, xPoints[2]]
            point4 = self.originalImage[i, xPoints[3]]
            point5 = self.originalImage[i, xPoints[4]]
            point6 = self.originalImage[i, xPoints[5]]
            point7 = self.originalImage[i, xPoints[6]]
            point8 = self.originalImage[i, xPoints[7]]

            lineStart = None
            if self.pixelIsBlack(point1) and self.pixelIsBlack(point2) and self.pixelIsBlack(point3) and self.pixelIsBlack(point4) and self.pixelIsBlack(point5) and self.pixelIsBlack(point6) and self.pixelIsBlack(point7) and self.pixelIsBlack(point8):
                lineStart = i
                while self.pixelIsBlack(point1) and self.pixelIsBlack(point2) and self.pixelIsBlack(point3) and self.pixelIsBlack(point4) and self.pixelIsBlack(point5) and self.pixelIsBlack(point6) and self.pixelIsBlack(point7) and self.pixelIsBlack(point8) and i+1 < shape[0]:
                    i = i + 1

                    point1 = self.originalImage[i, xPoints[0]]
                    point2 = self.originalImage[i, xPoints[1]]
                    point3 = self.originalImage[i, xPoints[2]]
                    point4 = self.originalImage[i, xPoints[3]]
                    point5 = self.originalImage[i, xPoints[4]]
                    point6 = self.originalImage[i, xPoints[5]]
                    point7 = self.originalImage[i, xPoints[6]]
                    point8 = self.originalImage[i, xPoints[7]]

                if lineStart or lineStart == 0:
                    horizontalLines.append((lineStart, i-1))
            i = i+1

        verticalLines = []
        i = 0
        while i < shape[1]:
            point1 = self.originalImage[yPoints[0], i]
            point2 = self.originalImage[yPoints[1], i]
            point3 = self.originalImage[yPoints[2], i]
            point4 = self.originalImage[yPoints[3], i]
            point5 = self.originalImage[yPoints[4], i]
            point6 = self.originalImage[yPoints[5], i]
            point7 = self.originalImage[yPoints[6], i]
            point8 = self.originalImage[yPoints[7], i]
            lineStart = None
            if self.pixelIsBlack(point1) and self.pixelIsBlack(point2) and self.pixelIsBlack(point3) and self.pixelIsBlack(point4) and self.pixelIsBlack(point5) and self.pixelIsBlack(point6) and self.pixelIsBlack(point7) and self.pixelIsBlack(point8):
                lineStart = i
                while self.pixelIsBlack(point1) and self.pixelIsBlack(point2) and self.pixelIsBlack(point3) and self.pixelIsBlack(point4) and self.pixelIsBlack(point5) and self.pixelIsBlack(point6) and self.pixelIsBlack(point7) and self.pixelIsBlack(point8) and i+1 < shape[1]:
                    i = i + 1

                    point1 = self.originalImage[yPoints[0], i]
                    point2 = self.originalImage[yPoints[1], i]
                    point3 = self.originalImage[yPoints[2], i]
                    point4 = self.originalImage[yPoints[3], i]
                    point5 = self.originalImage[yPoints[4], i]
                    point6 = self.originalImage[yPoints[5], i]
                    point7 = self.originalImage[yPoints[6], i]
                    point8 = self.originalImage[yPoints[7], i]

            if lineStart or lineStart == 0:
                verticalLines.append((lineStart, i-1))

            i = i+1

        return {"horizontalLines": horizontalLines, "verticalLines": verticalLines}

    def getCells(self):
        lines = self.findLines()
        horizontalLines = lines['horizontalLines']
        verticalLines = lines['verticalLines']
        cells = []
        for i in range(9):
            row = []
            for i in range(9):
                row.append(None)
            cells.append(row)

        for i in range(len(horizontalLines) - 1):
            horizontalCellBounds = (
                horizontalLines[i][1], horizontalLines[i+1][0])
            for j in range(len(verticalLines)-1):
                verticalCellBounds = (
                    verticalLines[j][1], verticalLines[j+1][0])
                cell = self.originalImage[horizontalCellBounds[0]:horizontalCellBounds[1],
                                          verticalCellBounds[0]:verticalCellBounds[1]]
                cells[i][j] = cell

        self.cells = cells
        return cells

    def getNumberedCells(self, modelLocation):

        if self.cells == None:
            self.getCells()

        digitClassifier = DigitClassifierNN()
        digitClassifier.loadModel(modelLocation)

        numberedCells = copy.deepcopy(self.cells)
        for i in range(len(numberedCells)):
            for j in range(len(numberedCells[i])):
                cell = self.cells[i][j]
                result = digitClassifier.predict(cell)
                numberedCells[i][j] = result

        self.numberedCells = numberedCells
        return numberedCells


if __name__ == "__main__":
    puzz = Puzzle(
        "/Users/patrickbell/Documents/sodukuAI/puzzleDetector/Sample3.png")
    numberedCells = puzz.getNumberedCells(
        '/Users/patrickbell/Documents/sodukuAI/digitClassifier/wholeModelSaveWith7Epochs')
    for i in range(len(numberedCells)):
        print(numberedCells[i])

    # NOTE: IT SEEMS THAT IT IS DETECTED SKINNY 4's AS 1'S. NEED TO TRAIN BETTER.
