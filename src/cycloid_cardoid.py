import cv2, sys
import numpy as np

def warp(p):

    P = np.zeros(p.shape, np.int32)

    x = p[0]
    y = p[1]

    P[0] = SCREEN_WIDTH - 1 - int(x * scale + bias)
    P[1] = SCREEN_HEIGHT - 1 - int(y * scale + bias)

    return P

def warpV(vp):

    VP = np.zeros(vp.shape, np.int32)

    for i in range(vp.shape[0]):

        VP[i] = warp(vp[i])

    return VP

def rotate2D(p, c, theta):

    q = p - c

    R = np.array([[np.cos(theta), -np.sin(theta)],
            [np.sin(theta), np.cos(theta)]])

    r = q@(R.T)

    s = r + c

    return s

def cycloid(p, r, c, theta):

    q = rotate2D(p, c, theta)

    if p.ndim > 1:
        q[:, 0] -= r * theta
    else:
        q[0] -= r * theta

    return q

def define_F_vertices(r):

    F = []
    
    R = r * 0.35

    F.append(( 1.5 * R,  2 * R))
    F.append((-1.5 * R,  2 * R))
    F.append((-1.5 * R,  1 * R))
    F.append(( 0.5 * R,  1 * R))
    F.append(( 0.5 * R,  0.5 * R))
    F.append((-0.75 * R,  0.5 * R))
    F.append((-0.75 * R, -0.5 * R))
    F.append(( 0.5 * R, -0.5 * R))
    F.append(( 0.5 * R, -1.75 * R))
    F.append(( 1.5 * R, -1.75 * R))

    return np.array(F)


fontFace = cv2.FONT_HERSHEY_SIMPLEX

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (255, 255, 0)
MAGENTA = (255, 0, 255)

THICKNESS = 1

r = 1.0

SCREEN_WIDTH = 512
SCREEN_HEIGHT = 512

scale = (SCREEN_HEIGHT - 100) / (3.5 * np.pi * r + 2 * r)
bias = SCREEN_HEIGHT / 2

screen = np.zeros((SCREEN_HEIGHT, SCREEN_WIDTH, 3), np.uint8)
screen2 = np.zeros((SCREEN_HEIGHT, SCREEN_WIDTH, 3), np.uint8)

R = int(r * scale)

orig = np.array((0, 0))
c0 = np.array((0, 2 * r))
p0 = np.array((0, 3 * r))
q0 = np.array((0, r))

f = define_F_vertices(r)

nDiv = 100

theta = 0
delta = np.pi * 2 / nDiv

p = []
q = []
key = -1

cv2.circle(screen2, warp(np.array((0, 0))), R, WHITE, THICKNESS * 2)

for i in range(nDiv+1):

    _f = cycloid(f + c0, r, c0, theta)

    F = warpV(_f)

    cv2.rectangle(screen, (0, 0), (SCREEN_WIDTH - 1, SCREEN_HEIGHT - 1), BLACK, -1)

    for j in range(F.shape[0]):

        k = j - 1
        cv2.line(screen, F[j], F[k], WHITE, THICKNESS)

    _c0 = cycloid(c0, r, c0, theta)
    C0 = warp(_c0)
    cv2.circle(screen, C0, R, WHITE, THICKNESS)

    _p0 = cycloid(p0, r, c0, theta)
    P0 = warp(_p0)
    cv2.circle(screen, P0, THICKNESS * 10, MAGENTA, -1)

    if len(p) > 1:
        P1 = warp(p[-1])
        cv2.line(screen2, P0, P1, MAGENTA, THICKNESS * 2)

    p.append(_p0)

    _q0 = q0.copy()
    _q0[0] = q0[0] - r * theta
    Q0 = warp(_q0)

    if len(q) > 1:
        Q1 = warp(q[-1])
        cv2.line(screen2, Q0, Q1, WHITE, THICKNESS)

    q.append(_q0)

    cv2.imshow('screen', screen + screen2)

    key = cv2.waitKey(10)

    if key == 27 or key == ord('q') or key == ord('Q'):
        break

    if cv2.getWindowProperty('screen', cv2.WND_PROP_VISIBLE) <= 0:
        break
    
    theta += delta

p = np.array(p)
q = np.array(q)


cv2.putText(screen2, text = 'Hit any key', org = (10, 30), fontFace = fontFace, fontScale = 1.0, color = (255, 255, 255), thickness = 2, lineType = cv2.LINE_4) 

cv2.imshow('screen', screen + screen2)
    
cv2.waitKey(0)

cv2.rectangle(screen, (0, 0), (SCREEN_WIDTH - 1, SCREEN_HEIGHT - 1), BLACK, -1)
cv2.rectangle(screen2, (0, 0), (SCREEN_WIDTH - 1, SCREEN_HEIGHT - 1), BLACK, -1)

cv2.circle(screen2, warp(np.array((0, 0))), R, WHITE, THICKNESS * 2)

theta = delta

pp = p.copy()
qq = q.copy()

prev_qqi = q0

for i in range(1, nDiv + 1):

    if i > 0:
        prev_qqi = qq[i-1]
    
    pp[i:] = rotate2D(pp[i:], prev_qqi, delta)
    qq[i:] = rotate2D(qq[i:], prev_qqi, delta)
    
    #pp[i:] += prev_ppi
    P = warpV(pp)

    
    #qq[i:] += prev_ppi
    Q = warpV(qq)

    cv2.rectangle(screen, (0, 0), (SCREEN_WIDTH - 1, SCREEN_HEIGHT - 1), BLACK, -1)

    for j in range(1, len(P)):

        cv2.line(screen, P[j-1], P[j], MAGENTA, THICKNESS * 2)
        cv2.line(screen, Q[j-1], Q[j], WHITE, THICKNESS)

    c = (pp[-1] + qq[-1]) * 0.5
    _f = rotate2D(f, orig, theta)
    #_f = cycloid(f + c, r, c, theta)

    F = warpV(_f + c)

    for j in range(F.shape[0]):

        k = j - 1
        cv2.line(screen, F[j], F[k], WHITE, THICKNESS)

    C = warp(c)
    cv2.circle(screen, C, R, WHITE, THICKNESS)

    PP = warp(pp[-1])
    cv2.circle(screen, PP, THICKNESS * 10, MAGENTA, -1)

    cv2.imshow('screen', screen + screen2)
    
    key = cv2.waitKey(10)
     
    if key == 27 or key == ord('q') or key == ord('Q'):
        break

    if cv2.getWindowProperty('screen', cv2.WND_PROP_VISIBLE) <= 0:
        break
    
    theta += delta

cv2.putText(screen2, text = 'Hit ESC-key to terminate', org = (10, 30), fontFace = fontFace, fontScale = 1.0, color = (255, 255, 255), thickness = 2, lineType = cv2.LINE_4) 

cv2.imshow('screen', screen + screen2)
    
while key != 27:
    key = cv2.waitKey(100)

cv2.destroyAllWindows()
