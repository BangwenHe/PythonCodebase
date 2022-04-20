import os
import sys

import cv2 as cv
import numpy as np


# image = cv.imread("samples/3/3_r258_x192_y257.jpg")
assert os.path.exists(sys.argv[1])
image = cv.imread(sys.argv[1])


# use opencv callback function to extract coordinates
def extract_coordinate(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        print(x, y)
        global image
        cv.circle(image, (x, y), 2, (0, 0, 255), -1)
        cv.putText(image, str(x) + "," + str(y), (x, y), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        cv.imshow("image", image)
    elif event == cv.EVENT_MOUSEMOVE:
        print(x, y)


cv.namedWindow("image", cv.WINDOW_GUI_NORMAL)
cv.setMouseCallback("image", extract_coordinate)

while True:
    cv.imshow("image", image)
    key = cv.waitKey(1)
    if key == ord("q"):
        break
