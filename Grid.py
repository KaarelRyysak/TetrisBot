import pyscreenshot as ImageGrab
import time
 
#User must change these varibles for specific screen size.
#Current values are set for 1920x1080 screens
x_pad = 89
y_pad = 302
x_width = 887
y_length = 894
 
#starting square for bottom left cell
x_start = 247
y_start = 557
 
#------------------------------------------------
 
gameMatrix = [[0 for x in range(10)] for y in range(20)] #matrix for game grid
 
 
def getGameState():
    pix = im.load()
 
    for y in range(20):
        for x in range(10):
            colour = pix[(x_start - 13 + (x * 26)), (y_start + 13 - (y * 26))]
            print(colour)
            if (colour[0] > 36 or colour[1] > 36 or colour [2] > 36):
                gameMatrix[y][x] = 1
        #----------------------------------------------------------------------#   
        if (x == 0):
            return
            #break scanning if whole row is empty to save time
    return
    #once done
 
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