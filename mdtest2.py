# Simple test of motor driver using dual-channel PWM control
# modelled on Adafruit simpletest.py by Tony Dicola
# Author: Matthew Cardinal
# License: Public Domain
#from __future__ import division
import time

# Import the PCA9685 module.
import Adafruit_PCA9685

# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

# Configure min and max servo pulse lengths
servo_min = 150  # Min pulse length out of 4096
servo_max = 1000  # Max pulse length out of 4096

# Helper function to make setting a servo pulse width simpler.
def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(300)
def forward():
    print('Forward!')
    pwm.set_pwm(15, 0, 4095)
    pwm.set_pwm(14, 0, 0)
    pwm.set_pwm(11, 0, 0)
    pwm.set_pwm(10, 0, 4095)

def backward():
    print('Reversing...')
    pwm.set_pwm(15, 0, 0)
    pwm.set_pwm(14, 0, 4095)
    pwm.set_pwm(11, 0, 4095)
    pwm.set_pwm(10, 0, 0)

def left():
    print("Left!")
    pwm.set_pwm(15, 0, 0)
    pwm.set_pwm(14, 0, 4095)
    pwm.set_pwm(11, 0, 0)
    pwm.set_pwm(10, 0, 4095)

def right():
    print("Right!")
    pwm.set_pwm(15, 0, 4095)
    pwm.set_pwm(14, 0, 0)
    pwm.set_pwm(11, 0, 4095)
    pwm.set_pwm(10, 0, 0)

def stop():
    print('Stop!')
    pwm.set_pwm(15, 0, 0)
    pwm.set_pwm(14, 0, 0)
    pwm.set_pwm(11, 0, 0)
    pwm.set_pwm(10, 0, 0)

pwm.set_pwm(13, 0, 2000)
pwm.set_pwm(9, 0, 2000)
print('Control system active...')
while True:
    command = raw_input('Enter f, b, l, r or s to control the motor, v xxx for speed, e to quit> ')
    if command[0] == 'f':
        forward()
    elif command[0] == 'b':
	backward()
    elif command[0] == 'l':
        left()
    elif command[0] == 'r':
        right()
    elif command[0] == 's':
        stop()
    elif command[0] == 'e':
        stop()
        exit()
    elif command[0] == 'v':
	n_command = command.split(' ')[1]
	if not n_command.isdigit():
		print('Choose a valid number between 0-100')
	else:
		n_command = int(n_command)
		print('Changing speed to: ' + str(n_command))
		n_command = max(min(int(n_command * 40.95), 4095), 0)
		pwm.set_pwm(13, 0, n_command)
		pwm.set_pwm(9, 0, n_command)
    else:
        print('Incorrect command. Please retry.')


