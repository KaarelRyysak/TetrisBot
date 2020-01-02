#All code for the release version is in this cell
#The release version will load the model from memory and start playing
#This version will not record the results or re-train the model
#It will only have the necessary imports
import multiprocessing

if __name__ == "__main__":
    multiprocessing.freeze_support() #Fixing pyinstaller
    
    import keras.models
    import math
    import pyscreenshot
    import time
    import pyautogui
    import cv2
    import numpy as np
    import copy
    import keras.utils

    #Let's define some functions to play the game and save the data
    #This finds the position of the game on the current screen
    def autoCalibrate():
        if __name__ == "__main__":
            topLeft  = pyautogui.locateOnScreen('hold.png')
            bottomRight = pyautogui.locateOnScreen('next.png')
            x_pad = topLeft[0] - 12
            y_pad = topLeft[1] - 47
            x_width = bottomRight[0] + 176
            y_length = bottomRight[1] + 550
            return (x_pad, y_pad, x_width, y_length)
        else:
            return None

    #This captures the screen and converts the gamefield into a matrix format
    def getAllBlocks():
        # Define the matrix for all the blocks
        x_size = 10
        y_size = 20
        gameMatrix = [[0 for x in range(x_size)] for y in range(y_size)]
        # Define the color that can't be a block
        black = (0,0,0)
        # Read the frame and translate it into HSV colorspace
        frame = cv2.imread("game.png")
        frame = frame[36:560, 214:482]
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # Fill the matrix with ones and zeros, so all the blocks would be displayed correctly
        for y in range(y_size):
            for x in range(x_size):
                x1 = 13 + (26*x)
                y1 = (560-36-13) - (26*y)
                r, g, b = frame[y1, x1]
                if (r,g,b) == black:
                    gameMatrix[y][x] = 0
                else:
                    gameMatrix[y][x] = 1
        return gameMatrix

    #This takes an image and figures out which tetromino is displayed
    #Then it returns an index for that tetromino
    def getNextBlock(frame):
        # Read in all the shape files and make them into grayscale
        yellow = cv2.imread("yellow.png")
        purple = cv2.imread("purple.png")
        red = cv2.imread("red.png")
        blue = cv2.imread("blue.png")
        teal = cv2.imread("teal.png")
        green = cv2.imread("green.png")
        orange = cv2.imread("orange.png")
        yellow = cv2.cvtColor(yellow, cv2.COLOR_BGR2GRAY)
        purple = cv2.cvtColor(purple, cv2.COLOR_BGR2GRAY)
        red = cv2.cvtColor(red, cv2.COLOR_BGR2GRAY)
        blue = cv2.cvtColor(blue, cv2.COLOR_BGR2GRAY)
        teal = cv2.cvtColor(teal, cv2.COLOR_BGR2GRAY)
        green = cv2.cvtColor(green, cv2.COLOR_BGR2GRAY)
        orange = cv2.cvtColor(orange, cv2.COLOR_BGR2GRAY)
        # Match the template wih the frame
        res1 = cv2.matchTemplate(frame,yellow,cv2.TM_CCOEFF_NORMED)
        res2 = cv2.matchTemplate(frame,purple,cv2.TM_CCOEFF_NORMED)
        res3 = cv2.matchTemplate(frame,red,cv2.TM_CCOEFF_NORMED)
        res4 = cv2.matchTemplate(frame,blue,cv2.TM_CCOEFF_NORMED)
        res5 = cv2.matchTemplate(frame,teal,cv2.TM_CCOEFF_NORMED)
        res6 = cv2.matchTemplate(frame,green,cv2.TM_CCOEFF_NORMED)
        res7 = cv2.matchTemplate(frame,orange,cv2.TM_CCOEFF_NORMED)
        # Determine whether the block was detected or not
        threshold = 0.8
        match1 = False
        if np.amax(res1) > threshold:
            match1 = True
        match2 = False
        if np.amax(res2) >= threshold:
            match2 = True
        match3 = False
        if np.amax(res3) >= threshold:
            match3 = True
        match4 = False
        if np.amax(res4) >= threshold:
            match4 = True
        match5 = False
        if np.amax(res5) >= threshold:
            match5 = True
        match6 = False
        if np.amax(res6) >= threshold:
            match6 = True
        match7 = False
        if np.amax(res7) >= threshold:
            match7 = True
        # Return the block number in order to determin what block was detected
        if match1:
            return 1
        elif match2:
            return 2
        elif match3:
            return 3
        elif match4:
            return 4
        elif match5:
            return 5
        elif match6:
            return 6
        elif match7:
            return 7
        else:
            #print("getNextBlock didn't match.")
            raise ValueError("getNextBlock didn't match.")
    #         print([res1, res2, res3, res4, res5, res6, res7])
    #         cv2.imshow('image',frame)
    #         cv2.waitKey(0)

    #This starts the game by pressing on the "play" button
    def startGame():
        x, y = pyautogui.locateCenterOnScreen('play.png')
        pyautogui.click(x, y)  

    #This function will make a move
    #x - how many squares to the right should the block be dropped? (0 to 9)
    def makeMove(x, x_pad, y_pad):
        pyautogui.click(x_pad+230 + 26*x, y_pad+100)  

    #This function will pause and quit the game
    def endGame(x_pad, y_pad):
        pyautogui.click(x_pad+700, y_pad+540)
        time.sleep(0.1)
        pyautogui.click(x_pad+360, y_pad+400)
        time.sleep(0.1)
        pyautogui.click(x_pad+360, y_pad+300) 

    #Get the height of the tower of blocks in the game matrix
    def getHeight(gameMatrix):
        matrix = gameMatrix[:14]
        height = 0
        for row in range(14):
            if matrix[row] != [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
                height += 1
        return height
            

    #Let's define some functions to process the data from the model

    #Code to read training data from the text document
    def readData():

        file = open("train_data.txt", "r")
        dataString = file.readlines()
        file.close()
        X = ast.literal_eval(dataString[0])
        y = ast.literal_eval(dataString[1])

        return (X, y)

    #Code for pre-processing the data
    def preProcessData(X, y=[]):
        #X = np.array(X)
        X = copy.deepcopy(X)
        y = copy.deepcopy(y)
        for i in range(len(X)):
            el = X[i]
            #Let's flatten the coordinate matrix so that it is easier to process
            newMatrix = np.array(el[0]).flatten()
            #Let's convert data for the tile to an appropriate one-hot vector
            currentTile = keras.utils.to_categorical([el[1]-1, 6])[0]
            #Now let's add these two lists together
            newMatrix = np.array(np.append(newMatrix, currentTile))
            X[i] = newMatrix
        
        if y != []:
            y = keras.utils,to_categorical(y)
        return (np.array(X), np.array(y))

    #Code for predicting the next move
    def predict(gameMatrix, currentBlock):
        moveState = [copy.deepcopy(gameMatrix[:10]), copy.copy(currentBlock)]
        modelInput = preProcessData([moveState])[0]
        result = model.predict(modelInput)[0]
        
        return np.argmax(result)
        
        

    
    model = keras.models.load_model("mudel.h5")
    numberOfGames = 10 #How many games will be played
    completedLines = 0 #Variable that stores the number of successful drops by bot
    #play the game using the model's predictions and makeMove()
    #Keep making moves in a loop. 
    #If the total height of the tower was reduced, save the move for training
    time.sleep(5) #Wait for 5 seconds so the user can start up the game
    x_pad, y_pad, x_width, y_length = autoCalibrate()
    for i in range(numberOfGames):
        print("Progress: game " + str(i+1) + " out of " + str(numberOfGames))

        startGame()
        time.sleep(1) #This is so the game will have time to load
        giveUp = False #This will be used to end the loop
        lastMove = None #Data about the previous move
        lastMoveState = None #State of the game at prev. move
        lastHeight = -1 #Height of the prev. gamestate

        #Let's get the current block during the countdown
        im=pyscreenshot.grab(bbox =(x_pad,y_pad,x_width,y_length))
        im.save("game.png")

        frame = cv2.imread("game.png")
        frame1 = frame[100:172, 546:668]
        frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        frame2 = frame[172:244, 546:668]
        frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        frame3 = frame[244:309, 546:668]
        frame3 = cv2.cvtColor(frame3, cv2.COLOR_BGR2GRAY)

        currentBlock = getNextBlock(frame1)

        time.sleep(3) #Let's wait for 3 more seconds so the countdown menu ends

        while not giveUp:
            im=pyscreenshot.grab(bbox =(x_pad,y_pad,x_width,y_length))
            im.save("game.png")

            frame = cv2.imread("game.png")
            frame1 = frame[100:172, 546:668]
            frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
            frame2 = frame[172:244, 546:668]
            frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
            frame3 = frame[244:309, 546:668]
            frame3 = cv2.cvtColor(frame3, cv2.COLOR_BGR2GRAY)

            gameMatrix = getAllBlocks()
            h = getHeight(gameMatrix)
            nextBlock1 = getNextBlock(frame1)
            nextBlock2 = getNextBlock(frame2)
            nextBlock3 = getNextBlock(frame3)

            #If the tower is over 10 blocks high, the bot ends the game
            if(h > 10):
                giveUp = True

            move = predict(gameMatrix, currentBlock)

            if(not giveUp):
                makeMove(move, x_pad, y_pad)

            #If the last move reduced the height of the tower,
            #it was a good move and will be recorded
            if(h < lastHeight):
                completedLines += 1

            #Save the current data for future use
            lastHeight = h
            lastMoveState = [copy.deepcopy(gameMatrix[:10]), copy.copy(currentBlock)]
            lastMove = move
            currentBlock = nextBlock1
        #close the game and start a new one
        endGame(x_pad, y_pad)

    print("The bot played " + str(numberOfGames) + " games and made " + str(completedLines) + " moves that completed a horizontal line.")
