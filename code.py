import board
import digitalio
import time
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# Set up a keyboard device.
kbd = Keyboard(usb_hid.devices)

while True:
    led.value = not led.value
    time.sleep(0.5)
    # Type lowercase 'a'. Presses the 'a' key and releases it.
    kbd.send(Keycode.A)