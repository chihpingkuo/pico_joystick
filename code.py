import board
import digitalio
import time
import math
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
led.value = True

# Set up a keyboard device.
kbd = Keyboard(usb_hid.devices)

while not i2c.try_lock():
    pass

joystick = MyJoystick2(i2c)
joystick.set_axis_x_invert()


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

W_state = False
A_state = False
S_state = False
D_state = False

try:
    while True:  
        
        # keypad
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
                
        # joystick
        pos = joystick.get_axis_position()
        x = pos[0]
        y = pos[1]
        angle_radians = math.atan2(y, x)
        angle_degrees = math.degrees(angle_radians)
        distance = math.sqrt(x**2 + y**2)
        print("x: {}, y: {}, deg: {}, dst: {}".format(x, y, angle_degrees, distance))
               
        threshold = 1024
               
        # right
        if 22.5 >= angle_degrees and angle_degrees > -22.5 and distance > threshold:
            print("right")
            
            if W_state:
                kbd.release(Keycode.W)
                W_state = False
            if A_state:
                kbd.release(Keycode.A)
                A_state = False
            if S_state:
                kbd.release(Keycode.S)
                S_state = False
            if not D_state:
                kbd.press(Keycode.D)
                D_state = True
            
        elif 67.5 >= angle_degrees and angle_degrees > 22.5 and distance > threshold*0.9:
            print("up right")
            
            if not W_state:
                kbd.press(Keycode.W)
                W_state = True
            if A_state:
                kbd.release(Keycode.A)
                A_state = False
            if S_state:
                kbd.release(Keycode.S)
                S_state = False
            if not D_state:
                kbd.press(Keycode.D)
                D_state = True
                
        elif 112.5 >= angle_degrees and angle_degrees > 67.5 and distance > threshold:
            print("up ")
            
            if not W_state:
                kbd.press(Keycode.W)
                W_state = True
            if A_state:
                kbd.release(Keycode.A)
                A_state = False
            if S_state:
                kbd.release(Keycode.S)
                S_state = False
            if D_state:
                kbd.release(Keycode.D)
                D_state = False
                
        elif 157.5 >= angle_degrees and angle_degrees > 112.5 and distance > threshold*0.9:
            print("up left")
            
            if not W_state:
                kbd.press(Keycode.W)
                W_state = True
            if not A_state:
                kbd.press(Keycode.A)
                A_state = True
            if S_state:
                kbd.release(Keycode.S)
                S_state = False
            if D_state:
                kbd.release(Keycode.D)
                D_state = False

        elif 180 >= angle_degrees and angle_degrees > 157.5 and distance > threshold:
            print("left")
            
            if W_state:
                kbd.release(Keycode.W)
                W_state = False
            if not A_state:
                kbd.press(Keycode.A)
                A_state = True
            if S_state:
                kbd.release(Keycode.S)
                S_state = False
            if D_state:
                kbd.release(Keycode.D)
                D_state = False

        elif -180 < angle_degrees and angle_degrees <= -157.5 and distance > threshold:
            print("left")
            
            if W_state:
                kbd.release(Keycode.W)
                W_state = False
            if not A_state:
                kbd.press(Keycode.A)
                A_state = True
            if S_state:
                kbd.release(Keycode.S)
                S_state = False
            if D_state:
                kbd.release(Keycode.D)
                D_state = False
                
        elif -157.5 < angle_degrees and angle_degrees <= -112.5 and distance > threshold*0.9:
            print("down left")
            
            if W_state:
                kbd.release(Keycode.W)
                W_state = False
            if not A_state:
                kbd.press(Keycode.A)
                A_state = True
            if not S_state:
                kbd.press(Keycode.S)
                S_state = True
            if D_state:
                kbd.release(Keycode.D)
                D_state = False
                
        elif -112.5 < angle_degrees and angle_degrees <= -67.5 and distance > threshold:
            print("down")
            
            if W_state:
                kbd.release(Keycode.W)
                W_state = False
            if A_state:
                kbd.release(Keycode.A)
                A_state = False
            if not S_state:
                kbd.press(Keycode.S)
                S_state = True
            if D_state:
                kbd.release(Keycode.D)
                D_state = False
                
        elif -67.5 < angle_degrees and angle_degrees <= -322.5 and distance > threshold*0.9:
            print("down right")
            
            if W_state:
                kbd.release(Keycode.W)
                W_state = False
            if A_state:
                kbd.release(Keycode.A)
                A_state = False
            if not S_state:
                kbd.press(Keycode.S)
                S_state = True
            if not D_state:
                kbd.press(Keycode.D)
                D_state = True
                
        else:
            if W_state:
                kbd.release(Keycode.W)
                W_state = False
            if A_state:
                kbd.release(Keycode.A)
                A_state = False
            if S_state:
                kbd.release(Keycode.S)
                S_state = False
            if D_state:
                kbd.release(Keycode.D)
                D_state = False
               
        # Type lowercase 'a'. Presses the 'a' key and releases it.
        # kbd.send(Keycode.A)
        time.sleep(0.05)    
    
finally:  # unlock the i2c bus when ctrl-c'ing out of the loop
    i2c.unlock()