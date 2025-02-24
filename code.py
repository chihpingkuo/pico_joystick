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

pins = [board.GP6,  board.GP7,  board.GP8,  board.GP9,
        board.GP10, board.GP11, board.GP12, board.GP13]
key_pin_array = []

for pin in pins:
    key_pin = digitalio.DigitalInOut(pin)
    key_pin.direction = digitalio.Direction.INPUT
    key_pin.pull = digitalio.Pull.UP
    key_pin_array.append(key_pin)

keycode_array = [Keycode.ONE, Keycode.TWO, Keycode.THREE, Keycode.FOUR,
                 Keycode.FIVE, Keycode.SIX, Keycode.SEVEN, Keycode.EIGHT]
    
key_state = [0,0,0,0,
             0,0,0,0]

try:
    while True:
        led.value = not led.value
        time.sleep(0.05)
              
        #print(joystick.get_axis_position())
        
        # Type lowercase 'a'. Presses the 'a' key and releases it.
        # kbd.send(Keycode.A)
        
        for i in range(8):
            if key_state[i] == 0:
                if not key_pin_array[i].value:
                    kbd.press(keycode_array[i])
                    key_state[i] = 1
            # key_state[i] == 1:
            else: 
                if key_pin_array[i].value:
                    kbd.release(keycode_array[i])
                    key_state[i] = 0
                                
            
    
finally:  # unlock the i2c bus when ctrl-c'ing out of the loop
    i2c.unlock()