import pyscreenshot as ImageGrab
import time
 
x_pad = 89
y_pad = 302
x_width = 887
y_length = 894
 
if __name__ == "__main__":
    print("Enter name of screen shot")
    filename = input()
    time.sleep(10)
    im=ImageGrab.grab(bbox =(x_pad,y_pad,x_width,y_length))
    im.save("./blocks/" + filename + ".png")
   