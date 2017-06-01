import RPi.GPIO as GPIO
import time
import os
from numpy import array

from random import randint

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

#Set up BCM mode for Pinout - "Broadcom SOC channel"
GPIO.setmode(GPIO.BCM)

#Set up our Pins
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Button 4
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Button 3
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Button 2
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)  #Button 1

#Set up our daisy chained display matrixes (MAX7219)
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=2, rotate=3) #rotate 1=90 / 2=180 / 3=270

# definitions of tetrominos
tetro_i = [(0,0), (1,0), (2,0), (3,0)]
tetro_o = [(0,0), (1,0), (1,1), (0,1)]
tetro_t = [(0,0), (1,0), (2,0), (1,1)]
tetro_l = [(0,0), (1,0), (2,0), (2,1)]
tetro_z = [(0,0), (1,0), (1,1), (2,1)]

tetrominos = []
tetrominos.append(tetro_i)
tetrominos.append(tetro_o)
tetrominos.append(tetro_t)
tetrominos.append(tetro_l)
tetrominos.append(tetro_z)

def offset(points, offset):
    output = []
    for i in range(len(points)):
        output.append((points[i][0] + offset[0]))
        output.append((points[i][1] + offset[1]))
    return output

def getRandomXOffset(points):
    upper = 0
    for i in range(len(points)):
        if(points[i][0] > upper):
            upper = points[i][0]
    return (randint(0, 7 - upper), 0)

def drawTetromino(draw):
    # random tetromino from list
    t = randint(0, len(tetrominos)-1)
    # random x
    x = randint(0, 7)
    y = 0

    # for each tetromino tuple
    points = offset(tetrominos[t], getRandomXOffset(tetrominos[t]))
    draw.point(points, fill="white")

    print("Tetronimo: ", str(t))
    print("Indent: ", str(x))


while True:
    if ( GPIO.input(26) == False ): #if button on GPIO26 is clicked
        #Define Message Var, for use in display output
        msg = ("Hello World!")

        #Output to console
        print("Button 4 Clicked")
        os.system('date') # print the systems date and time
        print(GPIO.input(26))
        time.sleep(.2)

        #Output to display matrixes
        with canvas(device) as draw:
            show_message(device, msg, fill="white", font=proportional(CP437_FONT),scroll_delay=0.1)

    if ( GPIO.input(19) == False ): #if button on GPIO19 is clicked
        #Output to console
        print("Button 3 Pressed")
        os.system('date') # print the systems date and time
        print(GPIO.input(19))
        time.sleep(.2)

        #Output to Display matrixes
        with canvas(device) as draw:
            draw.rectangle(device.bounding_box, outline="white", fill="black")

            # Draw a rectangle of lit up LEDs around the edge of the display,
            # fill the inside with unlit LEDs

    if ( GPIO.input(13) == False ):
        # Output to console
        print("Button 2 Pressed")
        print(GPIO.input(13))
        time.sleep(.2)

        # canvas
        with canvas(device) as draw:
            drawTetromino(draw)

    if ( GPIO.input(6) == False ):
        print("Button 1 Pressed")
        os.system('date') # print the systems date and time
        print(GPIO.input(6))
        time.sleep(.2)


