import ImageGrab
import os
import time
import win32api
import win32con
import ImageOps
from numpy import *


# This is designed to work on a resolution of 1440 x 900

# globals
x_pad = -1
y_pad = 113
endScreen=1439,859
counter=0
timePass=time.time()
data=[]


old=[]
points=[(482, 597), (142, 121), (152, 121), (161, 121),
        (169, 122), (179, 121), (179, 121), (186, 130),
        (178, 130), (170, 130), (162, 130), (153, 130),
        (150, 138), (163, 136), (167, 136), (178, 136)]
        


def mousePos(cord):
    #sets mouse position
    win32api.SetCursorPos((x_pad + cord[0], y_pad + cord[1]))
     
def get_cords():
    x,y = win32api.GetCursorPos()
    x = x - x_pad
    y = y - y_pad
    return (x,y)

    
def screenGrab():
    b1 = (x_pad+1,y_pad+1,x_pad+1439, y_pad+745)
    im = ImageGrab.grab(b1)
    return im

    
def main():
    global points, old, data
    win32api.GetAsyncKeyState(27)
    im=screenGrab()
    ans=time.time()
    for i in range(len(points)):
        old.append(im.getpixel(points[i]))
    while not win32api.GetAsyncKeyState(27):
        im=screenGrab()
        valid=0
        for i in range(len(points)):
            if old[i]!=im.getpixel(points[i]):
                valid=1
                break
        if valid:
            x=time.time()
            data.append(x-ans)
            print x-ans
            ans=x
            for i in range(len(points)):
                old[i]=im.getpixel(points[i])
        
        
        
        
        
 
if __name__ == '__main__':
##    reset()
    main()
