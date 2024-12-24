import cv2, sys
import numpy as np

SCREEN_SIZE = 512
MARGIN = 50
scale = 1.0
bias = 0.0

def warp(u):

    U = int(u * scale + bias)

    return U

def rotate2D(x, y, theta):

    X = np.cos(theta) * x - np.sin(theta) * y
    Y = np.sin(theta) * x + np.cos(theta) * y

    return X, Y

def spirograph(x, y, rL, rS, thetaL):

    thetaS = -thetaL * rL / rS

    x1, y1 = rotate2D(x, y, thetaS)
    x2 = x1 + rL - rS
    y2 = y1
    x3, y3 = rotate2D(x2, y2, thetaL)
    x4 = warp(x3)
    y4 = warp(y3)

    return x4, y4

def spirographV(V, rL, rS, thetaL):

    _V = []

    for v in V:

        x = v[0]
        y = v[1]

        X, Y = spirograph(x, y, rL, rS, thetaL)

        _V.append((X, Y))

    return _V

def generate_inner_point(r):

    x = np.random.rand() * r * 2 - r
    y = np.random.rand() * r * 2 - r

    while x ** 2 + y ** 2 > r ** 2:
    
        x = np.random.rand() * r * 2 - r
        y = np.random.rand() * r * 2 - r
    
    return x, y

def generate_rS(rL):

    rS = np.random.rand() * rL + 0.1

    cross = []
    cross.append((rS, 0))
    cross.append((-rS, 0))
    cross.append((0, rS))
    cross.append((0, -rS))

    return rS, cross

def getDelta(x, y, rS, nDiv):

    l = np.sqrt(x ** 2 + y ** 2)
    ratio = rS / l

    delta = np.pi * 2 * ratio / nDiv

    return delta

def main():

    global scale, bias

    argv = sys.argv
    argc = len(argv)

    print('%s draws intratrochoid curve (spirography)' % argv[0])
    print('[usage] python %s [<length>]' % argv[0])
    rL = 10.0
    
    WHITE = (255, 255, 255)
    CYAN = (255, 255, 0)
    #YELLOW = (0, 255, 255)
    #MAGENTA = (255, 0, 255)
    #ORANGE = (0, 128, 255)
    
    scale = (SCREEN_SIZE - MARGIN * 2) / (rL * 3)
    bias = SCREEN_SIZE / 2
    
    screen = np.zeros((SCREEN_SIZE, SCREEN_SIZE, 3), np.uint8)
    screen2 = np.zeros((SCREEN_SIZE, SCREEN_SIZE, 3), np.uint8)
    
    XC0 = warp(0)
    YC0 = warp(0)
    R0  = int(rL * scale)
    
    rS, cross = generate_rS(rL)
    
    xc1 = rL - rS
    yc1 = 0
    
    nDiv = 100
    
    key = -1
    
    thetaL = 0
    #delta = np.pi * 2 / nDiv
    
    xp, yp = generate_inner_point(rL) # (rS)
    
    delta = getDelta(xp, yp, rS, nDiv)
    
    prev_x = warp(xp + rL - rS)
    prev_y = warp(yp)
    
    print('Press ESC-key or Q-key to terminate')
    print('Press S-key to save screen image')
    print('Press +/- key to speed up/down')
    print('Press P-key to toggle pause')
    print('Press other key to reset Spirograph')
    
    terminate = False
    captureNo = 1
    wait_time = 5
    prev_wait_time = wait_time
    flag_pause = False
    
    PREVS = None
    
    while not terminate and key != 27 and key != ord('q') and key != ord('Q'):
    
        for i in range(nDiv):
        
            cv2.circle(screen, (XC0, YC0), R0, WHITE, 1)
        
            thetaL += delta
       
            CROSS = spirographV(cross, rL, rS, thetaL)        
            
            X0 = CROSS[0][0]
            Y0 = CROSS[0][1]
    
            X1 = CROSS[1][0]
            Y1 = CROSS[1][1]
    
            X2 = CROSS[2][0]
            Y2 = CROSS[2][1]
    
            X3 = CROSS[3][0]
            Y3 = CROSS[3][1]
    
            XC1 = (X0 + X1 + X2 + X3) // 4
            YC1 = (Y0 + Y1 + Y2 + Y3) // 4
    
            R1 = int(rS * scale) 
    
            cv2.line(screen, (X0, Y0), (X1, Y1), WHITE, 1)
            cv2.line(screen, (X2, Y2), (X3, Y3), WHITE, 1)
            cv2.circle(screen, (XC1, YC1), R1, WHITE, 1)
    
            XP, YP = spirograph(xp,yp, rL, rS, thetaL)
    
            cv2.circle(screen, (XP, YP), 5, CYAN, -1)
            cv2.line(screen, (XP, YP), (XC1, YC1), WHITE, 1)
            
            cv2.line(screen2, (XP, YP), (prev_x, prev_y), (255, 255, 0), 1)
    
            prev_x = XP
            prev_y = YP
    
            #cv2.imshow('screen', screen)
            #cv2.imshow('screen2', screen2)
            cv2.imshow('screen', screen + screen2)
            key = cv2.waitKey(wait_time)
       
            if key == 27 or key == ord('q') or key == ord('Q'):
                break
    
            if key != -1:
    
                if key == ord('s') or key == ord('S'):
    
                    capture_path = 'spirograph_%04d.png' % captureNo
                    cv2.imwrite(capture_path, screen2)
                    print('save %s' % capture_path)
                    print('xp:%f, yp:%f, rL:%f, rS:%f' % (xp, yp, rL, rS))
                    captureNo += 1
               
                elif key == ord('i') or key == ord('I'):
                    print('xp:%f, yp:%f, rL:%f, rS:%f' % (xp, yp, rL, rS))
                    
                elif key == ord('p') or key == ord('P'):
    
                    if flag_pause:
                        wait_time = prev_wait_time
                        flag_pause = False
                    else:
                        prev_wait_time = wait_time
                        wait_time = 0
                        flag_pause = True
    
                elif key == ord('-'):
                    if flag_pause:
                        wait_time = prev_wait_time
                        flag_pause = False
    
                    wait_time += 1
                    print('speed down: wait time %d (ms)' % wait_time)
    
                elif key == ord('+'):
                    if flag_pause:
                        wait_time = prev_wait_time
                        flag_pause = False
                    
                    wait_time -= 1
                    if wait_time < 1:
                        wait_time = 1
                    print('speed up: wait time %d (ms)' % wait_time)
    
                else:
    
                    rS, cross = generate_rS(rL)
    
                    xp, yp = generate_inner_point(rL) #(rS)
    
                    delta = getDelta(xp, yp, rS, nDiv)
    
                    prev_x = warp(xp + rL - rS)
                    prev_y = warp(yp)
    
                    thetaL = 0
    
                    screen2 = np.zeros((SCREEN_SIZE, SCREEN_SIZE, 3), np.uint8)
            
            if cv2.getWindowProperty('screen', cv2.WND_PROP_VISIBLE) <= 0:
                terminate = True
                break
            
            screen = np.zeros((SCREEN_SIZE, SCREEN_SIZE, 3), np.uint8)
    
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
