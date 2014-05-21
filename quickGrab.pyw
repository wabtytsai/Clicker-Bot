import ImageGrab
import os
import time

# globals

x_pad = 29
y_pad = 84

def screenGrab():
    box = (x_pad+1,y_pad+1,640,450)
    im = ImageGrab.grab(box)
    im.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) + '.png', 'PNG')
    
 
def main():
    screenGrab()
 
if __name__ == '__main__':
    main()
