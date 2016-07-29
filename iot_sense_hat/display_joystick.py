import sys
import time
from iot_sense_hat import SenseHat
from evdev import ecodes

class DisplayJoystick():
    def __init__(self):
        self.sense = SenseHat()

        # 0, 0 = Top left
        # 7, 7 = Bottom right
        self.UP_PIXELS = [[3, 0], [4, 0]]
        self.DOWN_PIXELS = [[3, 7], [4, 7]]
        self.LEFT_PIXELS = [[0, 3], [0, 4]]
        self.RIGHT_PIXELS = [[7, 3], [7, 4]]
        self.CENTRE_PIXELS = [[3, 3], [4, 3], [3, 4], [4, 4]]

        self.BLACK = [0, 0, 0]
        self.WHITE = [255, 255, 255]

    def set_pixels(self, pixels, col):
        '''
        Set the desired pixels of the col color
        :param col: The pixels color
        '''
        for p in pixels:
            self.sense.set_pixel(p[0], p[1], col[0], col[1], col[2])

    def handle_code(self, code, colour):
        '''
        Set the desired pixels depending on the joystick code
        :param colour:
        '''
        if code == ecodes.KEY_DOWN:
            self.set_pixels(self.DOWN_PIXELS, colour)
        elif code == ecodes.KEY_UP:
            self.set_pixels(self.UP_PIXELS, colour)
        elif code == ecodes.KEY_LEFT:
            self.set_pixels(self.LEFT_PIXELS, colour)
        elif code == ecodes.KEY_RIGHT:
            self.set_pixels(self.RIGHT_PIXELS, colour)
        elif code == ecodes.KEY_ENTER:
            self.set_pixels(self.CENTRE_PIXELS, colour)

