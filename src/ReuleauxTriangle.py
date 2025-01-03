import cv2, sys
import numpy as np

SCREEN_SIZE = 768

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (255, 255, 0)

nDivs = 12

wait_time = 5

def warp(x):

    X = scale * x + bias

    return int(X)

def warpV(points):
  
    P = []

    for p in points:

        X = warp(p[0])
        Y = warp(p[1])
        P.append((X, Y))

    return P

def rotate2D(x, y, theta):

    X = np.cos(theta) * x - np.sin(theta) * y
    Y = np.sin(theta) * x + np.cos(theta) * y

    return X, Y

def rotate2DV(points, theta):

    POINTS = []

    for p in points:

        X, Y = rotate2D(p[0], p[1], theta)
        POINTS.append((X, Y))

    return POINTS

def createReuleauxTriangle(r, nDivs):

    points = []

    x0 = r
    y0 = 0

    delta = np.pi / 3 / nDivs
    alpha = 0

    offsetX = r / 2
    offsetY = r * np.sqrt(3) / 4

    for i in range(nDivs):

        x, y = rotate2D(x0, y0, alpha)
        points.append((x - offsetX, -y + offsetY))

        alpha += delta

    x1, y1 = rotate2D(x0, y0, np.pi / 3)
    alpha = 0

    for i in range(nDivs):

        x, y = rotate2D(x1 - r, y1, alpha)
        points.append((x + r - offsetX, -y + offsetY))

        alpha += delta

    x2 = - r / 2
    y2 = - r * np.sqrt(3) / 2
    alpha = 0

    for i in range(nDivs):

        x, y = rotate2D(x2, y2, alpha)
        points.append((x + r /2 - offsetX, -y - r * np.sqrt(3) / 2 + offsetY))

        alpha += delta

    return points

r = 1.0

scale = SCREEN_SIZE / (r * 2 * 1.1)
bias = SCREEN_SIZE / 2

screen = np.zeros((SCREEN_SIZE // 2, SCREEN_SIZE, 3), np.uint8)
screen2 = np.zeros((SCREEN_SIZE // 2, SCREEN_SIZE, 3), np.uint8)

points = createReuleauxTriangle(r, nDivs)

theta = 0
key = -1

print('Hit any key to terminate')

while key == -1:

    p = rotate2DV(points, theta)
    P = warpV(p)
    P = np.array(P)
    minY = np.min(P[:,1])
    P[:, 1] -= minY

    for i in range(P.shape[0]):
 
        if i == P.shape[0] - 1:
            j = 0
        else:
            j = i + 1
        cv2.line(screen, P[i], P[j], CYAN, 2)

    xc, yc = np.mean(p, axis=0)
    XC = warp(xc)
    YC = warp(yc)
    cv2.circle(screen, (XC, YC - minY), 10, CYAN, -1)
    cv2.circle(screen2, (XC, YC - minY), 1, WHITE, -1)

    cv2.imshow('screen', screen + screen2) 
    key = cv2.waitKey(wait_time)

    cv2.rectangle(screen, (0, 0), (SCREEN_SIZE - 1, SCREEN_SIZE - 1), BLACK, -1)
    theta += np.pi / 100

    if theta > np.pi * 2:
        theta -= np.pi * 2
        cv2.rectangle(screen2, (0, 0), (SCREEN_SIZE - 1, SCREEN_SIZE - 1), BLACK, -1)

cv2.destroyAllWindows()


