import pyscreenshot as ImageGrab
import pyautogui
import time

def autoCalibrate ():
    topLeft  = pyautogui.locateOnScreen("C:/TetrisAI/TetrisBot/hold.png")
    bottomRight = pyautogui.locateOnScreen("C:/TetrisAI/TetrisBot/next.png")
 
    x_pad = topLeft[0] - 62
    y_pad = topLeft[1] - 47
    x_width = bottomRight[0] + 226
    y_length = bottomRight[1] + 550
 
    return (x_pad, y_pad, x_width, y_length)

if __name__ == "__main__":
    time.sleep(5)
 
    x_pad, y_pad, x_width, y_length = autoCalibrate()
 
    print("x_pad=" + str(x_pad) + " " + "y_pad=" + str(y_pad) + " " + "x_width=" + str(x_width) + " " + "y_length=" + str(y_length))
    im=ImageGrab.grab(bbox =(x_pad,y_pad,x_width,y_length))
    im.save("game.png")
    im.show()