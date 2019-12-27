import pyscreenshot as ImageGrab
import time
 
#User must change these varibles for specific screen size.
#Current values are set for 1920x1080 screens
x_pad = 89
y_pad = 302
x_width = 887
y_length = 894
 
x_start = 260
y_start = 546
x_end = 494
y_end = 51

x_boxes = 10
y_boxes = 20
 
gameMatrix = [[0 for x in range(x_boxes)] for y in range(y_boxes)]
 
def getGameState():
    pix = im.load()
 
    for y in range(y_boxes):
        for x in range(x_boxes):
            colour = pix[(x_start + (x * ((x_end-x_start) / x_boxes))), (y_start - (y * ((y_start-y_end) / y_boxes)))]
            print(colour)
            print(x_start + (x * ((x_end-x_start) / x_boxes)))
            print(y_start - (y * ((y_start-y_end) / y_boxes)))
            if (colour[0] > 36 or colour[1] > 36 or colour [2] > 36):
                gameMatrix[y][x] = 1  
 
if __name__ == "__main__":
    time.sleep(10)
    im = ImageGrab.grab(bbox =(x_pad,y_pad,x_width,y_length))
    #im.show()
    im.save("game.png")
    getGameState()
 
    for y in range (19,-1,-1):
        print ("\n")
        for x in range (0,10):
            print(gameMatrix[y][x], end='')