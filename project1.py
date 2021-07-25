import cv2
import numpy as np


cap = cv2.VideoCapture(0)
cap.set(3, 700)
cap.set(4, 500)
cap.set(10,200)

# [5,107,0,19,255,255]

myColors = [
            [0,0,0,179,108,42]
            ]
myColorValues = [[0,0,0]]

myPoints = []     #[x, y, colorId]

# [158,76,59,179,255,255]

# [59,76,158,179,255,255]
def findColor(img, myColors, myColorValues):
    imgHSV = cv2.cvtColor(img,cv2.COLOR_RGB2HSV)
    count = 0
    newPoints = []
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        x, y = getContours(mask)
        cv2.circle(imgResult, (x, y), 10, myColorValues[count], cv2.FILLED)

        if x!=0 and y != 0:
            newPoints.append([x, y, count])

        # cv2.imshow(str(color[0]), mask)
    return newPoints
def getContours(img):
    contours, hierarchy, = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area>500:
            # cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 2)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)

            x, y, w, h = cv2.boundingRect(approx)

    return x+w//2,y


def drawOnCanvas(myPoints,myColorValues):
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]), 10, myColorValues[point[2]], cv2.FILLED)


# cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 2)




while True:
    success, img = cap.read()
    imgResult = img.copy()
    newPoints = findColor(img, myColors, myColorValues)
    if len(newPoints) != 0:
        for newP in newPoints:
            myPoints.append(newP)

    if len(myPoints) != 0:
        drawOnCanvas(myPoints, myColorValues)
    cv2.imshow('video', imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
