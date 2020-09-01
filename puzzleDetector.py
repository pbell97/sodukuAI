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
from digitClassifier import DigitClassifierNN
import copy


class Puzzle:
    def __init__(self, imagePath):
        self.imagePath = imagePath
        self.originalImage = self.loadImage(self.imagePath)
        self.blackLower = (0, 0, 0)
        self.blackUpper = (200, 200, 200)
        self.gridCorners = ((), (), (), ())
        self.coppedImageWithGrid = None
        self.cells = None
        self.numberedCells = None

    # Returns cv2 image from path
    def loadImage(self, path):
        return cv2.imread(path)

        # TODO: Debug Display image

    # Updates upper and lower black colors for mask
    def findGridColor(self):
        threshhold = 0.4
        for i in range(self.originalImage.shape[0]):
            color = self.originalImage[i][i]
            if color[0] < 200 and color[1] < 200 and color[2] < 200:
                self.blackLower = (
                    color[0]-color[0]*threshhold, color[1]-color[1]*threshhold, color[2]-color[2]*threshhold)
                self.blackUpper = (
                    color[0]+color[0]*threshhold, color[1]+color[1]*threshhold, color[2]+color[2]*threshhold)
                break

        # TODO: Debug lower & upper values here

    # Assigns the grid's corners and crops to just grid
    def cropToGrid(self):
        self.findGridColor()
        mask = cv2.inRange(self.originalImage,
                           self.blackLower, self.blackUpper)
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
        self.gridCorners = (topLeftCornerX, topLeftCornerY,
                            bottomRightCornerX, bottomRightCornerY)
        self.coppedImageWithGrid = self.originalImage[topLeftCornerY:
                                                      bottomRightCornerY, topLeftCornerX:bottomRightCornerX]

        # TODO: Debug show corners and copped image

    # Get images of all cells
    def getCells(self):
        self.cropToGrid()

        subGrids = [
            [[], [], []],
            [[], [], []],
            [[], [], []]
        ]

        # Creates list of subgrids
        height, width, colorChannels = self.coppedImageWithGrid.shape
        xInc = int(height/3)
        yInc = int(width/3)
        for i in range(3):
            for j in range(3):
                subGrids[i][j] = self.coppedImageWithGrid[yInc *
                                                          i:yInc*i+yInc, xInc*j:xInc*j+xInc]

        # All the cells, in a subgrid organication
        cells = []

        # Creates datastructure with same num of cells
        for subGridRow in range(3):
            cells.append([])
            for subGridColumn in range(3):
                cells[subGridRow].append([])
                for row in range(3):
                    cells[subGridRow][subGridColumn].append([])
                    for column in range(3):
                        cells[subGridRow][subGridColumn][row].append(None)

        # Assigns picture to each cell in datastructure
        for subGridRow in range(3):
            for subGridColumn in range(3):
                subGridImg = subGrids[subGridRow][subGridColumn]
                subGridImgHeight, subGridImgWidth, subGridImgColorChannels = subGridImg.shape
                xInc = int(subGridImgHeight/3)
                yInc = int(subGridImgWidth/3)
                for i in range(3):
                    for j in range(3):
                        cells[subGridRow][subGridColumn][i][j] = subGridImg[yInc *
                                                                            i:yInc*i+yInc, xInc*j:xInc*j+xInc]

        self.cells = cells

    # Shows the loaded picture
    def showOriginalPicture(self):
        self.__showImage(self.originalImage, "Original Image")

    # Shoes the cropped grid
    def showCroppedGrid(self):
        self.__showImage(self.croppedImageWithGrid, "Grid")

    # Displays image of a specific cell
    def showCell(self, num1, num2, num3, num4):
        self.__showImage(self.cells[num1][num2][num3][num4], "Cell")

    # Shows a given image
    def __showImage(self, image, title):
        cv2.imshow(title, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # Converts images to numbers
    def detectNumbers(self, model):
        # Recreates all the cells

        numberedCells = copy.deepcopy(self.cells)

        for subGridRow in range(3):
            for subGridColumn in range(3):
                for i in range(3):
                    for j in range(3):
                        numberedCells[subGridRow][subGridColumn][i][j] = model.predict(
                            self.cells[subGridRow][subGridColumn][i][j])

        self.numberedCells = numberedCells


if __name__ == "__main__":
    puzzle = Puzzle(
        "/Users/patrickbell/Documents/sodukuAI/puzzleDetector/Sample1.png")
    puzzle.getCells()
    # puzzle.showCell(0, 0, 2, 0)

    digitsNN = DigitClassifierNN()
    digitsNN.loadModel(
        '/Users/patrickbell/Documents/sodukuAI/digitClassifier/wholeModelSave')

    print(digitsNN.predict(puzzle.cells[0][0][2][0]))
    puzzle.detectNumbers(digitsNN)
    print(puzzle.numberedCells[0][0][2][0])
