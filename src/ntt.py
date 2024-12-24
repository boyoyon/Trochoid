import cv2, sys
import numpy as np

def warp(p):

    x = p[0]
    y = p[1]

    X = SCREEN_WIDTH - 1 - int(x * scale + bias)
    #Y = SCREEN_HEIGHT - 1 - int(y * scale + bias)
    Y = int(y * scale + bias)

    P = [X, Y]

    return P

def warpV(vp):

    VP = []

    for p in vp:

        P = warp(p)

        VP.append(P)

    return VP

def rotate2D(p, theta):

    x = p[0]
    y = p[1]

    X = np.cos(theta) * x - np.sin(theta) * y
    Y = np.sin(theta) * x + np.cos(theta) * y

    return [X, Y]

def rotate2DV(vp, theta):

    VQ = []

    for p in vp:

        q = rotate2D(p, theta)

        VQ.append(q)

    return VQ

def translate(p, r, theta):

    x = p[0]
    y = p[1]

    return [x - r * theta, y]

def cycloid(p, r, theta):

    q = rotate2D(p, theta)

    q[0] -= r * theta

    return q

def cycloidV(vp, r, theta):

    vq = []

    for p in vp:

        q = cycloid(p, r, theta)

        vq.append(q)

    return vq

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (255, 255, 0)
MAGENTA = (255, 0, 255)
RED = ( 64, 128, 255)

r = 1.0

SCREEN_WIDTH = 512
SCREEN_HEIGHT = 512

scale = SCREEN_HEIGHT / ((4 * np.pi * r + 2 * r) * 1.1)
bias = SCREEN_HEIGHT / 2

screen = np.zeros((SCREEN_HEIGHT, SCREEN_WIDTH, 3), np.uint8)
screen2 = np.zeros((SCREEN_HEIGHT, SCREEN_WIDTH, 3), np.uint8)

R = int(r * scale)

p0 = (0, 2.5 * r)

nDiv = 100

delta = np.pi * 2 / nDiv

p = []
key = -1

theta = 0

for i in range(nDiv+1):
   
    _p0 = cycloid(p0, r, theta)
    P0 = warp(_p0)
    #cv2.circle(screen, P0, 40, RED, -1)

    if len(p) > 1:
        P1 = warp(p[-1])
        cv2.line(screen2, P0, P1, RED, 20)

    p.append(_p0)

    cv2.imshow('screen', 255 - screen - screen2)

    key = cv2.waitKey(10)

    if key == 27 or key == ord('q') or key == ord('Q'):
        break

    if cv2.getWindowProperty('screen', cv2.WND_PROP_VISIBLE) <= 0:
        break
    
    cv2.rectangle(screen, (0, 0), (SCREEN_WIDTH - 1, SCREEN_HEIGHT - 1), BLACK, -1)

    theta += delta

p = np.array(p)

cv2.rectangle(screen, (0, 0), (SCREEN_WIDTH - 1, SCREEN_HEIGHT - 1), BLACK, -1)
cv2.rectangle(screen2, (0, 0), (SCREEN_WIDTH - 1, SCREEN_HEIGHT - 1), BLACK, -1)

pp = p.copy()

for i in range(1, nDiv):

    prev_ppi = pp[i-1]
    
    pp[i:] = rotate2DV(pp[i:] - prev_ppi, delta)
    pp[i:] += prev_ppi
    P = warpV(pp)

    for j in range(1, len(P)):

        cv2.line(screen, P[j-1], P[j], RED, 20)

    cv2.imshow('screen', 255 - screen - screen2)
    
    key = cv2.waitKey(10)
     
    if key == 27 or key == ord('q') or key == ord('Q'):
        break

    if cv2.getWindowProperty('screen', cv2.WND_PROP_VISIBLE) <= 0:
        break
    
    cv2.rectangle(screen, (0, 0), (SCREEN_WIDTH - 1, SCREEN_HEIGHT - 1), BLACK, -1)

key = cv2.waitKey(0)

cv2.destroyAllWindows()
