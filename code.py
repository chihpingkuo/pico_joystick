import board
import digitalio
import time
import struct
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# To create I2C bus on specific pins
import busio
i2c = busio.I2C(board.GP1, board.GP0)    # Pi Pico RP2040

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# Set up a keyboard device.
kbd = Keyboard(usb_hid.devices)

while not i2c.try_lock():
    pass

try:
    while True:
        led.value = not led.value
        time.sleep(1)
        # Type lowercase 'a'. Presses the 'a' key and releases it.
        #kbd.send(Keycode.A)
                
        # _read_reg_data
        buf = bytearray(1)
        buf[0] = 0x00
        time.sleep(0.001)
        i2c.writeto(0x63, buf)
        buf = bytearray(4)
        i2c.readfrom_into(0x63, buf)
        x, y = struct.unpack("<hh", buf)
        print('-----')
        print(x)
        print(y)
    
finally:  # unlock the i2c bus when ctrl-c'ing out of the loop
    i2c.unlock()