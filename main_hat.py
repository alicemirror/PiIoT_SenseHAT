'''
Main SenseHAT management for PiIoT project.

This application executes a series of initial actions then start polling the sensors and react to the sensors movement
accordingly with the project features.
'''

from hat_manager import Screen, EnvironmentStatus, Joystick
from utility import IPStuff
from hat_rainbow import HatRainbow
from display_joystick import DisplayJoystick
import time

def joystickDispatcher(keycode, status):
    '''
    Joystick dispatched method. Exectues the corresopnding function depending on the keycode passed
    if keycode is none the thread should stop

    :param keycode: Keycode ID
    :param status: Keycode Status (On/Off etc.)
    '''
    print(keycode, status)

    joyDisplay = DisplayJoystick()

    if keycode is not 0:
        joyDisplay.handle_code(keycode, joyDisplay.WHITE)
        time.sleep(0.25)
    else:
        hatScreen.clear()


#   Main application entry point
#
if __name__ == '__main__':
    # # Startup message
    hatScreen = Screen()
    hatScreen.clear()
    # hatScreen.startup()
    #
    # # Sensors
    # hatSensors = EnvironmentStatus()
    # print ("Avg Temp = ", hatSensors.getAvgTemperature())
    # print ("Global Env = ", hatSensors.getEnvironment())
    #
    # # Node IP address
    # nodeIP = IPStuff()
    # hatScreen.clear()
    # hatScreen.msg(nodeIP.getHostName() + " - " + nodeIP.getIP())
    #
    # # Joystick
    # joy = Joystick()
    #
    # # Executes the joystick control in the main application
    # # CTRL-C to stop and go ahead
    # print("Joystick is running in the main thread. Press CTRL-C to end")
    # joy.loopJoystick(joystickDispatcher)

    # Executes the joystick control in a separate thread
    joyThread = Joystick(joystickDispatcher, 1)
    print("Joystick will be launched in a separate thread. Press CTRL-C to end")
    joyThread.start()

    # Start the rainbow loop in the main thread
    print("Rainbow will run in the main thread")
    rainbow = HatRainbow()
    counter = 5000
    while counter is not 0:
        rainbow.rainbow()
        counter -= 1

    hatScreen.clear()

    print("Press CTRL-Z to exit")
