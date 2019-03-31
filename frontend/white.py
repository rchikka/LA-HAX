
# tester python script for frontend

import cv2


def isWhite1(filename):
    image = cv2.imread(filename)
    if cv2.countNonZero(image) == 0:
        print("Image is black")
    else:
        print("Colored image")


def isWhite2(filename):
    image = cv2.imread(filename)
    if cv2.countNonZero(image) == 0:
        return 0
    else:
        return 1

# isWhite1("banana1.jpg")
# isWhite2("banana1.jpg")