import board
import digitalio
import time
import struct
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
import busio
from MyJoystick2 import MyJoystick2

# To create I2C bus on specific pins
i2c = busio.I2C(board.GP1, board.GP0)    # Pi Pico RP2040

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# Set up a keyboard device.
kbd = Keyboard(usb_hid.devices)

while not i2c.try_lock():
    pass

joystick = MyJoystick2(i2c)

try:
    while True:
        led.value = not led.value
        time.sleep(0.1)
              
        print(joystick.get_axis_position())
        
        # Type lowercase 'a'. Presses the 'a' key and releases it.
        # kbd.send(Keycode.A)
            
    
finally:  # unlock the i2c bus when ctrl-c'ing out of the loop
    i2c.unlock()