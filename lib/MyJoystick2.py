from busio import I2C
import struct
import time

class MyJoystick2:
    """
    note:
        en: The joystick is an input unit for control, utilizing an I2C communication interface and supporting three-axis control signals (X/Y-axis analog input for displacement and Z-axis digital input for key presses). It is ideal for applications like gaming and robot control.
        cn: 操纵杆是一种控制输入单元，采用I2C通信接口，支持三轴控制信号输入（X/Y轴位移的模拟输入和Z轴按键的数字输入）。适用于游戏、机器人控制等应用场景。

    details:
        color: "#0FE6D7"
        link: ""
        image: ""
        category: Unit

    example: |
        from unit import Joystick2Unit
        from hardware import *
        i2c = I2C(1, scl=22, sda=21)
        joystick = Joystick2Unit(i2c)
        joystick.read_adc_value()
        joystick.read_button_status()
        joystick.set_rgb_led(255, 0, 0)
        joystick.get_rgb_led()
        joystick.set_deadzone_position(200, 200)
        while True:
            joystick.read_axis_position()
    """
    def __init__(self, i2c: I2C, address: int | list | tuple = 0x63):
        """
        note: Initialize the Joystick2 Unit.

        label:
            en: "%1 initialize Joystick2 Unit with I2C %2, address %3"
            cn: "%1 初始化 Joystick2 Unit，使用I2C %2，地址 %3"

        params:
            i2c:
              note: I2C port to use.
            address:
              note: I2C address of the Joystick2 Unit.
        """
        self._color = [0, 0, 0]
        self._br = 1
        self._i2c = i2c
        self._addr = address
        self._x_inv = False
        self._y_inv = False
        self._swap = False
        self._x_mapping = [0, 0, 0, 0]
        self._y_mapping = [0, 0, 0, 0]
        if self._addr not in self._i2c.scan():
            raise Exception("Joystick2Unit not found, please check if it's properly connected.")
        
    def _read_reg_data(self, reg: int = 0, num: int = 0) -> bytearray:
        buf = bytearray(1)
        buf[0] = reg
        # time.sleep_ms(1)
        time.sleep(0.001)
        self._i2c.writeto(self._addr, buf)
        buf = bytearray(num)
        self._i2c.readfrom_into(self._addr, buf)
        return buf
    
    def set_axis_x_invert(self, invert: bool = True) -> None:
        """
        note: Invert the X-axis of the joystick.

        label:
            en: "%1 invert X-axis %2"
            cn: "%1 反转 X 轴 %2"

        params:
            invert:
              note: Whether to invert the X-axis.
        """
        self._x_inv = invert

    def set_axis_y_invert(self, invert: bool = True) -> None:
        """
        note: Invert the Y-axis of the joystick.

        label:
            en: "%1 invert Y-axis %2"
            cn: "%1 反转 Y 轴 %2"

        params:
            invert:
              note: Whether to invert the Y-axis.
        """
        self._y_inv = invert
    
    def get_axis_position(self) -> tuple:
        """
        note: Read the position of the joystick.

        label:
            en: "%1 read position of Joystick"
            cn: "%1 读取 Joystick 的位置"

        return:
            note: Returns a tuple of the X-axis and Y-axis positions. The range is -4096 to 4096.
        """
        buf = self._read_reg_data(0x50, 4)
        x, y = struct.unpack("<hh", buf)
        if self._x_inv:
            x = -x
        if self._y_inv:
            y = -y
        if self._swap:
            x, y = y, x
        return (x, y)