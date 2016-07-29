'''
SenseHAT management classes

A set of classes and methods to manage the device properties

'''

from iot_sense_hat import SenseHat
from evdev import InputDevice, list_devices, ecodes
import time
from threading import Thread

'''
Constants
'''
SCROLL_SPEED = 0.1
DEBUG = True
STARTUP = "PiIoT v. 0.1, Balearic Dynamics"
STARTUP_COLOR = [20, 20, 128]
JOYSTICK_NAME = "Raspberry Pi Sense HAT Joystick"

'''
Manage the SenseHAT environment status
This class includes a series of methods with a high level APIs methods to simplify the management of the display
and the sensors, finalised to the IoT application
'''
class EnvironmentStatus():
    def __init__(self):
        '''
        Initializes the SenseHAT settings
        '''
        self.sense = SenseHat()

    def getAvgTemperature(self):
        '''
        Get the enrionmental temperature.
        Acquire the three different temperature values (temperature, temp from pressure and temp from humidity)
        then return the calcualted average value
        :return:
        '''

        p_temp = self.sense.get_temperature_from_pressure()
        h_temp = self.sense.get_temperature_from_humidity()
        t_temp = self.sense.get_temperature()

        temp = (p_temp + h_temp + t_temp) / 3

        return temp

    def getEnvironment(self):
        '''
        Retrieve the environmental sensors status.
        Two values of temperature are returned in the tuple; the first is the absolute temperature value from
        the temperature sensor while the second is the average calculated temperature
        :return:
        '''

        humidity = self.sense.get_humidity()
        t_temp = self.sense.get_temperature()
        pressure = self.sense.get_pressure()
        avg_temperature = self.getAvgTemperature()

        return humidity, pressure, t_temp, avg_temperature

'''
Detect the object movement creating the position data mapping.
Data mapping than can be converted in a colour-relative display on the SenseHAT
or can be sent as-is to the dynamic surface controller.
'''
class Movement():
    def __init__(self):
        '''

        '''
        self.sense = SenseHat()

'''
Screen setting utilities
'''
class Screen():
    def __init__(self):
       '''

       '''
       self.sense = SenseHat()

    def clear(self, color = None):
        '''
        Clear the HAT display. Optionally it is possible to fill the display with a predefined
        colour and define an alpha level
        :param color: A list in the format (r, g, b) with values between 0-255
        '''
        if color is not None:
            self.sense.clear(color)
        else:
            self.sense.clear()

    def startup(self):
        '''
        Show the startup message and system version, then clear the screen
        '''
        self.msg(STARTUP, STARTUP_COLOR)
        self.clear()

    def msg(self, text = "", color = None, background = None, speed = None):
        '''
        Scroll the text string on the display
        :param color: A list in the format (r, g, b) with values between 0-255
        :param background: A list in the format (r, g, b)
        '''
        if color is not None:
            txt_col = color
        else:
            txt_col = [255, 255, 255]

        if background is not None:
            txt_back = background
        else:
            txt_back = [0, 0, 0]

        if speed is not None:
            txt_speed = speed
        else:
            txt_speed = SCROLL_SPEED

        if DEBUG:
            print ("show_message : ", text, txt_speed, txt_col, txt_back)

        self.sense.show_message(text, txt_speed, txt_col, txt_back)

'''
Joystick events controller
'''
class Joystick(Thread):
    def __init__(self, disptach_event = None, threadID=0):
        '''
        Initialises parameters to manage the joystick asynchornously.
        When this thread class is instantiated the thread ID should be passed to it
        '''
        self.sense = SenseHat()
        self.device = None

        # Check for the joystick presence
        devices = [InputDevice(fn) for fn in list_devices()]
        for dev in devices:
            if dev.name == JOYSTICK_NAME:
                self.device = dev # Device found!
                break

        if self.device is None:
            if DEBUG:
                print('Raspberry Pi Sense HAT Joystick not found. Aborted')
        else:
            # If the dispatch event method callback has not been specified, the thread is not started
            if disptach_event is not None:
                # Initializes the thread parent class and get the thread ID parameter
                self.dispatch = disptach_event
                Thread.__init__(self)
                self.threadID = threadID
                if DEBUG:
                    print('Thread.__init__()')

    def run(self):
        '''
        Thread start overriding the Thread method
        '''
        if DEBUG:
            print("Joystick thread starting")
        # loop the joystick status
        try:
            for event in self.device.read_loop():
                # Return the event keycode and the value (up / down)
                self.dispatch(event.code, event.value)
        except KeyboardInterrupt:  # CTRL-C halt the loop. For testing purposes only
            if DEBUG:
                print("Joystick control ended by user. Thread stopped")

    def loopJoystick(self, dispatch_event):
        '''
        Manages the joystick input events. For better perfomances this method can be exectued in a
        separate thread; use the run method instead.
        When an event occurs, the dispatch_event function is called
        '''
        try:
            for event in self.device.read_loop():
                # Return the event keycode and the value (up / down)
                dispatch_event(event.code, event.value)
        except KeyboardInterrupt: # CTRL-C halt the loop. For testing purposes only
            if DEBUG:
                print("Joystick control ended by user")

