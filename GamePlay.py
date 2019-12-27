import pyautogui
import time
 
 
def startGame ():
    x, y = pyautogui.locateCenterOnScreen('play.png')
    pyautogui.click(x, y)
 
def quickDrop ():
    pyautogui.press('space')
 
def holdSwap ():
    pyautogui.press('shift')
 
def spin ():
    pyautogui.press('up')
 
def moveLeft():
    pyautogui.press('left')
 
def moveRight():
    pyautogui.press('right')
 
 
 
startGame()
time.sleep(3.2)
 
for x in range (0,4):
    moveLeft()
 
quickDrop()
holdSwap()