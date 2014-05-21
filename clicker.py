import ImageGrab
import os
import time
import win32api
import win32con
import ImageOps
import random
from numpy import *


# This is designed to work on a resolution of 1440 x 900

# globals
x_pad = -1
y_pad = 113
endScreen=1439,859
counter=0
timePass=0
timer=0

autoClick=False
pPressed=False
leftPressed=False


class Player:
    cookies=0.0
    cps=0
    upgrade=[[0,0] for i in range(10)]
    
class Building:
    bPos=[( 1253 , 126 ), ( 1244 , 175 ), ( 1234 , 232 ), ( 1242 , 286 ), ( 1254 , 357 ),
          ( 1254 , 403 ), ( 1250 , 469 ), ( 1238 , 519 ), ( 1244 , 590 ), ( 1252 , 643 )]
    bName=["Cursor", "Grandma", "Farm", "Factory", "Mine", "Shipment", "Alchemy Lab", "Protal", "Time machine", "Antimatter Condenser"]
    bCost=[15, 100, 500, 3000, 10000, 40000, 200000, 1666666, 123456789, 3999999999]
    bNum=[0]*10
    bCPS=[0.1, 0.5, 4, 10, 40, 100, 400, 6666, 98765, 999999]
    
class Cord:
    UPGRADE=(1165,50)
    BIG_COOKIE = (216, 331)
    MENU = (478, 17)
    SAVE = (483, 213)
    STATS = (497, 70)
    RESET = (470, 280)

def pause(n):
    global timePass
    time.sleep(n)
##    timePass+=n

def reset():
    global counter, timePass, autoClick
    Player.cookies=0.0
    Player.cps=0
    Player.upgrade=[[0,0] for i in range(10)]
    Building.bCost=[15, 100, 500, 3000, 10000, 40000, 200000, 1666666, 123456789, 3999999999]
    Building.bNum=[0]*10
    counter=0
    timePass=0
    autoClick=False
    mousePos(Cord.MENU)
    leftClick()
    time.sleep(0.1)
    mousePos(Cord.RESET)
    leftClick()
    time.sleep(0.1)
    mousePos((761, 112))
    leftClick()
    time.sleep(0.1)
    mousePos(Cord.MENU)
    leftClick()
    time.sleep(0.1)

def getBestBuilding():
    #gets costs for each CPS, the smaller the better
    best=Building.bCost[0]/Building.bCPS[0]
    pos=0
    limit=Player.cps*300+Player.cookies
    for i in range(1,10):
        if Building.bCost[i]<=limit and Building.bCost[i]/Building.bCPS[i] < best:
            best = Building.bCost[i]/Building.bCPS[i]
            pos = i
    return pos

def buyBuilding(n):
    mousePos(Building.bPos[n])
    leftClick()
    Player.cookies-=round(Building.bCost[n])
    Player.cps+=Building.bCPS[n]
    Building.bCost[n]*=1.15
    Building.bNum[n]+=1
    print("Buying "+Building.bName[n])

def checkUpgrade(im):
    global timePass
    noUpgradeColour=(36, 96, 129)
    upgradeYes=(0, 0, 0)
    upgradeNo=(14, 36, 48)
    firstUp=(1165,50)
    if im.getpixel(firstUp)==upgradeYes:
        mousePos(firstUp)
        leftClick()
        pause(0.05)
    
def saveProgress():
    global timePass
    #save current game progress
    mousePos(Cord.MENU)
    leftClick()
    pause(0.05)
    mousePos(Cord.SAVE)
    leftClick()
    pause(0.05)
    mousePos(Cord.MENU)
    leftClick()
    pause(0.05)
    
def clickCookie():
    if autoClick:
        mousePos(Cord.BIG_COOKIE)
        leftClick()
        Player.cookies+=1
        pause(0.05)
        #time.sleep(.01)

def leftClick():
    global timePass
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    pause(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
##    print "left Click."
    
def leftDown():
    global timePass
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    pause(0.05)
##    print 'left Down'
         
def leftUp():
    global timePass
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    pause(0.05)
##    print 'left release'

def rightClick():
    global timePass
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)
    pause(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)
##    print "right Click."   
    
def rightDown():
    global timePass
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)
    pause(0.05)
##    print 'right Down'
         
def rightUp():
    global timePass
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)
    pause(0.05)
##    print 'right release'

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
    ##im.save(os.getcwd() + '\\Snap__' + str(int(time.time())) +'.png', 'PNG')
    ##im.getpixel((x,y))
    return im

def roundUp(n):
    if n==int(n): return n
    return int(n)+1
    
def main():
    global counter,timePass, autoClick, pPressed, leftPressed, timer
    win32api.GetAsyncKeyState(ord('P'))
    win32api.GetAsyncKeyState(27)
    timer=time.time()+(1+(100*random.random()-50)*3/10000)
##    timer=time.time()+(1+(100*random.random()-85)*3/10000)
##    timePass=timer
    while not win32api.GetAsyncKeyState(27):

        clickCookie()
        best = getBestBuilding()
        if Player.cookies>1+Building.bCost[best]:
            buyBuilding(best)

        if pPressed and win32api.GetAsyncKeyState(ord('P'))==0:
            pPressed=False
            if autoClick:
                Player.cookies-=1
                autoClick=False
            else:
                autoClick=True
        if not pPressed and win32api.GetAsyncKeyState(ord('P'))!=0:
            pPressed=True

        if leftPressed and win32api.GetAsyncKeyState(win32con.MK_LBUTTON)==0:
            leftPressed = False
            curPos=get_cords()
            if 155<=curPos[0]<=272 and 230<=curPos[1]<=357:
                Player.cookies+=1
        if not leftPressed and win32api.GetAsyncKeyState(win32con.MK_LBUTTON)!=0:
            leftPressed = True
        
        
        counter+=1
        if counter%10==0:
            print Player.cps
            print Player.cookies
        if counter==1000:
            saveProgress()
            counter=0
        
        pause(0.05)
        if(time.time()>=timer):
            Player.cookies+=Player.cps
            timer=time.time()+(1+(100*random.random()-50)*3/10000)
##            timer=time.time()+(1+(100*random.random()-85)*3/10000)
##        ans=(time.time()-test)*(1+(10*(random.random())-8)*3/100)
##        Player.cookies+=ans*Player.cps
##        print ans
##        timePass=0
    
        
 
if __name__ == '__main__':
##    reset()
    main()
