# SPDX-FileCopyrightText: 2022 bborncr for CRCibernetica
#
# SPDX-License-Identifier: MIT

"""
`ideaboard`
================================================================================
CircuitPython helper library for the CRCibernetica IdeaBoard.
* Author(s): Bentley Born
Implementation Notes
--------------------
**Hardware:**
* `CRCibernetica IdeaBoard <https://www.crcibernetica.com/crcibernetica-ideaboard/`_
**Software and Dependencies:**
* CircuitPython firmware for IdeaBoard:
  https://circuitpython.org/board/crcibernetica_ideaboard/
* Adafruit's NeoPixel library: https://github.com/adafruit/Adafruit_CircuitPython_NeoPixel
* Adafruit's SimpleIO library: https://github.com/adafruit/Adafruit_CircuitPython_SimpleIO
* Adafruit's Motor library: https://github.com/adafruit/Adafruit_CircuitPython_Motor
"""
import board
from neopixel import NeoPixel
from rainbowio import colorwheel
import pwmio
from simpleio import map_range
from adafruit_motor import servo, motor
import digitalio
import analogio


class IdeaBoard:
    UP = digitalio.Pull.UP
    DOWN = digitalio.Pull.DOWN
    
    def __init__(self):
        self._brightness = 0.3
        self._np = NeoPixel(board.NEOPIXEL, 1, brightness=self._brightness, auto_write=True)
        self._np[0] = (0,0,0)
        self._m1a = pwmio.PWMOut(board.IO12, duty_cycle=0, frequency=50)
        self._m1b = pwmio.PWMOut(board.IO14, duty_cycle=0, frequency=50)
        self._m2a = pwmio.PWMOut(board.IO13, duty_cycle=0, frequency=50)
        self._m2b = pwmio.PWMOut(board.IO15, duty_cycle=0, frequency=50)
        self.motor_1 = motor.DCMotor(self._m1a, self._m1b)
        self.motor_2 = motor.DCMotor(self._m2a, self._m2b)
        self.map_range = map_range
    
    
    @property
    def pixel(self):
        return self._np[0]
    
    
    @pixel.setter
    def pixel(self, color=(0,0,0)):
        self._np[0] = color
    
    
    @property
    def brightness(self):
        return self._brightness
    
    
    @brightness.setter
    def brightness(self, new_brightness):
        if new_brightness <= 1 or new_brightness >= 0:
            self._brightness = new_brightness
            self._np.brightness = self._brightness
   
   
    @property
    def arcoiris(self):
        return self._np[0]
 
 
    @arcoiris.setter
    def arcoiris(self, n=0):
        color = colorwheel(n)
        self.pixel = color 
        
        
    class Servo:
        """
        A simple class for controlling hobby servos.

        Args:
            pin: The pin where servo is connected. Must support PWM.
            freq (int): The frequency of the signal, in hertz, normally 50Hz.
            min_pulse (int): The minimum signal length supported by the servo.
            max_pulse (int): The maximum signal length supported by the servo.
            angle (int or float): The angle of the servo in degrees.
        
        Usage:
            import board
            from ideaboard import IdeaBoard()
            ib = IdeaBoard()
            servo = ib.Servo(board.IO4)
            servo.angle = 45
            print(servo.angle)

        """
        def __init__(self, pin, freq=50, min_pulse = 500, max_pulse = 2500):
            self.min_pulse = min_pulse
            self.max_pulse = max_pulse
            self.us = 0
            self.freq = freq
            self._angle = 0
            self.pwm = pwmio.PWMOut(pin, duty_cycle=2 ** 15, frequency=freq)
            self.servo = servo.Servo(self.pwm, min_pulse = self.min_pulse, max_pulse = self.max_pulse)

        @property
        def angle(self):
            return self._angle
        
        @angle.setter
        def angle(self, new_angle):
            """Move to the specified angle in ``degrees``."""
            self._angle = new_angle
            self.servo.angle = self._angle
            
            
    class DigitalIn:
        """
        Create a digital input pin.

        Args:
            pin: The digital pin to set up. ie. board.IO4
            pull: internal resistor setting: ib.UP, ib.DOWN or None
        
        Usage:
            import board
            from ideaboard import IdeaBoard
            ib = IdeaBoard()
            pin = ib.DigitalIn(board.IO27)
            print(pin.value)

        """
        def __init__(self, pin, pull=None):
            self.digitalin = digitalio.DigitalInOut(pin)
            self.digitalin.direction = digitalio.Direction.INPUT
            if pull:
               self.digitalin.pull = pull
                

        @property
        def value(self):
            return self.digitalin.value
            

    class DigitalOut:
        """
        Create a digital output pin.

        Args:
            pin: The digital pin to set up. ie. board.IO4

        Usage:
            import board
            from ideaboard import IdeaBoard
            ib = IdeaBoard()
            pin = ib.DigitalOut(board.IO27)
            pin.value = True

        """
        def __init__(self, pin):
            self.digitalout = digitalio.DigitalInOut(pin)
            self.digitalout.direction = digitalio.Direction.OUTPUT
            self._value = 0

        @property
        def value(self):
            return self._value
        
        @value.setter
        def value(self, new_value):
            """Set the value of the output: True, False, 0 or 1"""
            self._value = new_value
            self.digitalout.value = self._value
            
            
    class AnalogIn:
        """
        Create an analog input pin.

        Args:
            pin: The analog pin to set up. ie. board.IO33
            
        Usage:
            import board
            from ideaboard import IdeaBoard
            ib = IdeaBoard()
            pin = ib.AnalogIn(board.IO33)
            print(pin.value)

        """
        def __init__(self, pin):
            self.analogin = analogio.AnalogIn(pin)

        @property
        def value(self):
            return self.analogin.value
        
        
    class AnalogOut:
        """
        Create an analog output pin (DAC).

        Args:
            pin: The analog pin to set up. There are two
            pins allowed on the IdeaBoard: board.IO25 or board.IO26
            
        Usage:
            import board
            from ideaboard import IdeaBoard
            ib = IdeaBoard()
            dac = ib.AnalogOut(board.IO26)
            dac.value = 32768 # sends 1.65V to the pin

        """
        def __init__(self, pin):
            self.analogout = analogio.AnalogOut(pin)

        @property
        def value(self):
            return self.analogOut.value
        
        @value.setter
        def value(self, new_value):
            """Set the value of the output: 0 - 65535"""
            #self._value = new_value
            self.analogout.value = new_value
            
