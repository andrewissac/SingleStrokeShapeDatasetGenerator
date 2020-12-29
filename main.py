import cv2 as cv
import numpy as np
import random
import argparse
import uuid
import os
from utils import mkdir, mouseInRect

# TO END THIS SCRIPT YOU'LL PROBABLY HAVE TO USE ESC ON YOUR KEYBOARD!
# example usage in terminal:
# python .\main.py --outdir D:\MyDataset --outputName Circle

parser = argparse.ArgumentParser()
parser.add_argument('--outputDir', required=False, type=str, default="",
                    help='Output directory to put the images in')
parser.add_argument('--outputName', required=True, type=str,
                    help='Output name of images')
args = parser.parse_args()

# region global variables
outputName = args.outputName
outputDir = os.path.join(args.outputDir, outputName)

bigOutputSize = 128, 128
bigOutputSizeFolderName = str(bigOutputSize[0]) + "x" + str(bigOutputSize[1])
bigOutputDir = os.path.join(outputDir, bigOutputSizeFolderName)

smallOutputSize = 64, 64
smallOutputSizeFolderName = str(
    smallOutputSize[0]) + "x" + str(smallOutputSize[1])
smallOutputDir = os.path.join(outputDir, smallOutputSizeFolderName)

mkdir(outputDir)
mkdir(bigOutputDir)
mkdir(smallOutputDir)

drawing = False  # true if mouse is pressed
rMouseBtnDown = False
ix, iy = -1, -1

width = 1600
height = 900

strokeColor = (255, 255, 255)
strokeThickness = 3
backgroundColor = (0, 0, 0)
rects = []
# endregion


def mouseCallback(event, x, y, flags, param):
    # mouse callback function
    global ix, iy, drawing, strokeThickness, strokeColor, rMouseBtnDown

    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
        strokeThickness = random.randint(1, 10)

    elif event == cv.EVENT_RBUTTONDOWN:
        rMouseBtnDown = True
        for rect in reversed(rects):
            if mouseInRect(x, y, rect):
                rectX, rectY, w, h = rect
                img[rectY:rectY+h, rectX:rectX+w] = (0, 0, 0)
                del rect

    elif event == cv.EVENT_RBUTTONUP:
        rMouseBtnDown = False

    elif event == cv.EVENT_MOUSEMOVE:
        if drawing == True:
            cv.line(img, (ix, iy), (x, y), color=strokeColor,
                    thickness=strokeThickness)
            ix, iy = x, y
        if rMouseBtnDown:
            for rect in reversed(rects):
                if mouseInRect(x, y, rect):
                    rectX, rectY, w, h = rect
                    img[rectY:rectY+h, rectX:rectX+w] = (0, 0, 0)
                    del rect

    elif event == cv.EVENT_LBUTTONUP:
        drawing = False
        cv.line(img, (ix, iy), (x, y), color=strokeColor,
                thickness=strokeThickness)


img = np.zeros((height, width, 3), np.uint8)
cv.namedWindow('image')
cv.setMouseCallback('image', mouseCallback)

while cv.getWindowProperty('image', 0) >= 0:
    img2 = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    contours, hierarchy = cv.findContours(
        img2, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    rects = []
    for c in contours:
        rects.append(cv.boundingRect(c))

    # region keyboard input
    key = cv.waitKey(30) & 0xFF

    # user pressed backspace
    if key == 8:
        # fill image with black
        img[:] = backgroundColor
        print("CLEARED CANVAS")

    # user pressed enter
    elif key == 13:
        for rect in rects:
            x, y, w, h = rect
            shapeID = uuid.uuid4()

            # extract shape based, resize and apply binarization
            ret, bigShape = cv.threshold(
                cv.resize(img[y:y+h, x:x+w], bigOutputSize, interpolation=cv.INTER_LINEAR), 30, 255, cv.THRESH_BINARY)
            ret_, smallShape = cv.threshold(
                cv.resize(img[y:y+h, x:x+w], smallOutputSize, interpolation=cv.INTER_LINEAR), 30, 255, cv.THRESH_BINARY)
            # save extracted shape
            cv.imwrite(os.path.join(
                bigOutputDir, "{}_{}.png".format(outputName, shapeID)), bigShape)
            cv.imwrite(os.path.join(smallOutputDir,
                                    "{}_{}.png".format(outputName, shapeID)), smallShape)
        print("SAVED IMAGES")
        img[:] = backgroundColor
        print("CLEARED CANVAS")

    # user pressed esc
    if key == 27:
        print("ESC")
        break
    # endregion

    boxesImg = img.copy()
    for rect in rects:
        x, y, w, h = rect
        cv.rectangle(boxesImg, (x, y),
                     (x + w, y + h), (0, 0, 255), 2)
    cv.imshow('image', boxesImg)


cv.destroyAllWindows()
