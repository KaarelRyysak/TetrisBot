import math
from PIL import Image
import pyscreenshot as ImageGrab
import time
import pyautogui

nextBlock1 = [660,142]
nextBlock2 = [660,210]
nextBlock3 = [660,276]
currentBlock = [386,75]
holdBlock = [136,140]

#please change
#User must change these varibles for specific screen size.
#Current values are set for 1920x1080 screens
x_pad = 556
y_pad = 352
x_width = 1348
y_length = 944
 
#starting square for bottom left cell
x_start = 279
y_start = 542
#-------------------------------------
 
gameMatrix = [[0 for x in range(10)] for y in range(20)]
 
def rgb2hsv(r, g, b):
    #converts rgb to hsv
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
 
    if mx == 0:
        s = 0
    else:
        s = df/mx
   
    return (int(h),int(((s*10)*10)))
 
 
def getBlockType (rgb_value):
    #enter in a rgb list and returns the colour of that block
 
    h,s = rgb2hsv(rgb_value[0],rgb_value[1],rgb_value[2])
    print(s)
 
 
    if (h >=285 and h <=305):
        #purple colour
        print("purple")
        return(1)
    elif (h >= 200 and h <=212):
        #blue colour
        print("blue")
        return(2)
    elif (h >= 180 and h <=190):
        #light blue colour
        print("light blue")
        return(3)
    elif (h >= 130 and h <=141):
        #green colour
        print("green")
        return(4)
    elif (h >= 50 and h <=60):
        #yellow colour
        print("yellow")
        return(5)
    elif (h >= 35 and h <=45):
        #orange colour
        print("orange")
        return(6)
    elif (h >= 0 and h <=2 and s >= 20):
        #red colour
        print("red")
        return(7)
    elif (h == 0 and s == 0):
        print("Invalid Cords")
    else:
        print("")
        return(0)
 
def getNextBlocks ():
    nextBlocks = [0,0,0]
    nextBlocks[0] = getBlockType(pix[nextBlock1[0],nextBlock1[1]])
    nextBlocks[1] = getBlockType(pix[nextBlock2[0],nextBlock2[1]])
    nextBlocks[2] = getBlockType(pix[nextBlock3[0],nextBlock3[1]])
    return(nextBlocks)
 
def getCurrnetBlock():
    return(getBlockType(pix[currentBlock[0],currentBlock[1]]))
 
def getHoldBlock():
    return(getBlockType(pix[holdBlock[0],holdBlock[1]]))
 
def autoCalibrate ():
    topLeft  = pyautogui.locateOnScreen('hold.png')
    bottomRight = pyautogui.locateOnScreen('next.png')
 
    x_pad = topLeft[0] - 62
    y_pad = topLeft[1] - 47
    x_width = bottomRight[0] + 226 #far right of image
    y_length = bottomRight[1] + 550 #far bottom of image
 
    return (x_pad, y_pad, x_width, y_length)
 
 
def startGame ():
    x, y = pyautogui.locateCenterOnScreen('play.png')
    pyautogui.click(x, y)  
 
 
if __name__ == "__main__":
 
    sleep(5)
    #im=ImageGrab.grab(bbox=(10,10,510,510)) # X1,Y1,X2,Y2
 
    x_pad, y_pad, x_width, y_length = autoCalibrate()
    startGame()
    sleep(2.36)
 
    #sleep(2)
    im=ImageGrab.grab(bbox =(x_pad,y_pad,x_width,y_length))
    #im.show()
   
    im.save("game.png")
    #im = Image.open("GAMESCREEN.png")
    pix = im.load()
 
 
#-------------------------------------
    # test statement to get data.
    print(getNextBlocks())
    #print(getHoldBlock())
    #print(getCurrnetBlock())
#--------------------------------------