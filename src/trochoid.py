import cv2, random, sys
import numpy as np

SCREEN_WIDTH = 800
SCREEN_HEIGHT = -1
    
scale = -1.0
bias = -1.0
    
def warp(u):

    U = int(u * scale + bias)

    return U

def rotate2D(x, y, theta):

    theta += np.pi

    X = np.cos(theta) * x - np.sin(theta) * y
    Y = np.sin(theta) * x + np.cos(theta) * y

    return X, Y

def trochoid(x, y, r, theta):

    x1, y1 = rotate2D(x, y, theta)
    x2 = x1 + r * theta
    y2 = y1
    x3 = warp(x2)
    y3 = warp(y2)

    return x3, y3

def trochoidV(V, r, theta):

    _V = []

    for v in V:

        x = v[0]
        y = v[1]

        X, Y = trochoid(x, y, r, theta)

        _V.append((X, Y))

    return _V

def generate_point(r):

    theta = random.random() * np.pi * 2.0

    x, y = rotate2D(0, r, theta)

    return x, y

def generate_f(r):

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

    return F

def main():

    global SCREEN_WIDTH, scale, bias

    argv = sys.argv
    argc = len(argv)
    
    print('%s draws trochoid curve' % argv[0])
    print('[usage] python %s [<length(2.0)>]' % argv[0])
    
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    
    length = 2.0
    if argc > 1:
        length = float(argv[1])

    r = 3.0
    
    SCREEN_HEIGHT = int(SCREEN_WIDTH/(np.pi + 1))
    
    scale = SCREEN_HEIGHT / (r * (length + 1) * 2)
    bias = SCREEN_HEIGHT / 2
    
    R = int(r * scale)
    
    screen = np.zeros((SCREEN_HEIGHT, SCREEN_WIDTH, 3), np.uint8)
    screen2 = np.zeros((SCREEN_HEIGHT, SCREEN_WIDTH, 3), np.uint8)
    
    x = 0
    y = r * length
    
    COLOR = (255, 255, 0)
    
    f = generate_f(r)
    
    nDiv = 200
    
    key = -1
    
    theta = 0
    delta = np.pi * 10 / nDiv
    
    print('Press ESC-key or Q-key to terminate')
    print('Press P-key to toggle pause/play')
    print('Press other key to step forward in pause mode')
    
    terminate = False
    captureNo = 1
    wait_time = 20
    prev_wait_time = wait_time
    flag_pause = False
    flag_init_pause = True

    while not terminate and key != 27 and key != ord('q') and key != ord('Q'):
    
        theta = 0
        PrevX = -1
        PrevY = -1

        for i in range(nDiv):
        
            X, Y = trochoid(x, y, r, theta)        
   
            if X > SCREEN_WIDTH:
                break

            cv2.circle(screen, (X, Y), 10, COLOR, -1)
   
            if PrevX >= 0 and PrevY >= 0:
                cv2.line(screen2, (X, Y), (PrevX, PrevY), COLOR, 2)
   
            center = trochoid(0, 0, r, theta)

            if length > 1.0:
                cv2.line(screen, (X, Y), center, WHITE, 2) 

            PrevX = X
            PrevY = Y
            
            F = trochoidV(f, r, theta)

            for j in range(len(F)-1):
                k = j + 1
                cv2.line(screen, F[j], F[k], WHITE, 1)
    
            cv2.line(screen, F[0], F[-1], WHITE, 1)
           
            XC, YC = trochoid(0, 0, r, theta)
            
            cv2.circle(screen, (XC, YC), R, WHITE, 1)
           
            Y0 = warp(r)
            cv2.line(screen, (0, Y0), (SCREEN_WIDTH - 1, Y0), WHITE, 1)
            
            #cv2.imshow('screen', screen)
            #cv2.imshow('screen2', screen2)
            cv2.imshow('screen', screen + screen2)
           
            if cv2.getWindowProperty('screen', cv2.WND_PROP_VISIBLE) <= 0:
                terminate = True
                break
         
            if flag_pause or flag_init_pause:
                key = cv2.waitKey(0)
                flag_init_pause = False
            else:
                key = cv2.waitKey(wait_time)
       
            if key == 27 or key == ord('q') or key == ord('Q'):
                terminate = True
                break
    
            elif key == ord('p') or key == ord('P'):

                flag_pause = not flag_pause

            cv2.rectangle(screen, (0, 0), (SCREEN_WIDTH - 1, SCREEN_HEIGHT -1), BLACK, -1)
    
            theta += delta
           
        flg_init_pause = True

        key = cv2.waitKey(0)
            
        if key == ord('s') or key == ord('S'):

            cv2.imwrite('trochoid.png', screen2)
            print('Save trochoid.png')

        cv2.rectangle(screen, (0, 0), (SCREEN_WIDTH - 1, SCREEN_HEIGHT -1), BLACK, -1)
        cv2.rectangle(screen2, (0, 0), (SCREEN_WIDTH - 1, SCREEN_HEIGHT -1), BLACK, -1)
    
        x, y = generate_point(r * length)

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

