import cv2 as cv
import numpy as np
import random

drawing = False  # true if mouse is pressed
ix, iy = -1, -1

width = 800
height = 500

strokeColor = (255, 255, 255)
strokeThickness = 3
backgroundColor = (0, 0, 0)

# mouse callback function


def drawStroke(event, x, y, flags, param):
    global ix, iy, drawing, strokeThickness, strokeColor

    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
        strokeThickness = random.randint(1, 15)

    elif event == cv.EVENT_MOUSEMOVE:
        if drawing == True:
            cv.line(img, (ix, iy), (x, y), color=strokeColor,
                    thickness=strokeThickness)
            ix, iy = x, y

    elif event == cv.EVENT_LBUTTONUP:
        drawing = False
        cv.line(img, (ix, iy), (x, y), color=strokeColor,
                thickness=strokeThickness)


img = np.zeros((height, width, 3), np.uint8)
cv.namedWindow('image')
cv.setMouseCallback('image', drawStroke)

while cv.getWindowProperty('image', 0) >= 0:
    key = cv.waitKey(30) & 0xFF
    # user pressed backspace
    if key == 8:
        # fill image with black
        img[:] = (0, 0, 0)
        print("CLEARED IMAGE")
    # user pressed enter
    if key == 13:
        print("ENTER")

    # user pressed esc
    # elif key == 27:
    #     print("ESC")
    #     break

    im2
    contours, hierarchy = cv.findContours(
        img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    cv.drawContours(img, contours, -1, (0, 255, 0), 3)
    cv.imshow('image', img)


cv.destroyAllWindows()
