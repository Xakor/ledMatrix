from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text, show_message
import RPi.GPIO as GPIO
import random
import time

class Snake:
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

    fps = 15
    # 0=>7
    width = 8
    # 0=>15
    height = 16

    # Snake with DEFAULT start
    snake = [(width / 2, height / 2)]
    speed = 1
    # 0=NORTH, 1=EAST, 2=SOUTH, 3=WEST
    facing = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    direction = 0

    score = 0
    prey = (random.randint(0, width - 1), random.randint(0, height - 1))


    def turnLeft(self):
        if (self.direction == 0):
            self.direction = len(self.facing) - 1
        else:
            self.direction -= 1
        self.forward()


    def turnRight(self):
        if (self.direction == len(self.facing) - 1):
            self.direction = 0
        else:
            self.direction += 1
        self.forward()

    def forward(self):
        if (self.snake[0] == self.prey):
            self.score += 1
            nextPlacement = (self.snake[0][0] + self.facing[self.direction][0], self.snake[0][1] + self.facing[self.direction][1])
            self.snake.insert(0, nextPlacement)
            self.prey = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))

        if (len(self.snake) > 0):
            for i in range(len(self.snake)-1):
                #print(len(self.snake))
                if (i != 0 and self.snake[0] == self.snake[i]):
                    print("I = ", i)
                    self.reset()

        for i in range(self.speed):
            nextPlacement = (self.snake[0][0] + self.facing[self.direction][0], self.snake[0][1] + self.facing[self.direction][1])
            self.snake.insert(0, nextPlacement)
            self.snake.pop()

        # Wraparound
        if (self.direction == 0 and self.snake[0][1] == -1): # North
            pos = (self.snake[0][0], self.height - 1)
            self.snake.insert(0, pos)
            self.snake.pop()
        elif (self.direction == 1 and self.snake[0][0] == self.width): # East
            pos = (0, self.snake[0][1])
            self.snake.insert(0, pos)
            self.snake.pop()
        elif (self.direction == 2 and self.snake[0][1] == self.height): # South
            pos = (self.snake[0][0], 0)
            self.snake.insert(0, pos)
            self.snake.pop()
        elif (self.direction == 3 and self.snake[0][0] == -1): # West
            pos = (self.width, self.snake[0][1])
            self.snake.insert(0,pos)
            self.snake.pop()

    def reset(self):
        self.snake = [(self.width / 2, self.height / 2)]
        self.direction = 0
        self.score = 0
        self.prey = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))

    def drawGame(self):
        with canvas(self.device) as draw:
            draw.point(self.snake, fill="white")
            draw.point(self.prey, fill="white")

    # Constructor
    def __init__(self):
        last = 0.
        nextMove = 0.
        command = "";
        while (True):
            # Seconds since the epoch (Timestamp)
            now = time.time()

            # Time Delta (s)
            dt = now - last
            last = now

            # Add Delta to "Timer" (Cooldown)
            nextMove += dt

            # Inputs
            if (GPIO.input(13) == False):
                print("Turn Right")
                command = "R"
            elif (GPIO.input(6) == False):
                print("Turn Left")
                command = "L"

            # Timer due
            if (nextMove > .5):
                print ("Next move triggered")
                # TRIGGER
                self.drawGame()
                if (command == "R"):
                    self.turnRight()
                elif (command == "L"):
                    self.turnLeft()
                elif (command == ""):
                    self.forward()
                command = ""

                # TRIGGER

                # Reset
                nextMove = 0.

            # Time until next frame
            sleepTime = 1. / self.fps - dt

            if (sleepTime > 0):
                time.sleep(sleepTime)

snake = Snake()