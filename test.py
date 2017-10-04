#!/usr/bin/pythonRoot
#This is a script


#flup helps implement fastcgi, which lets our requests run quickly
#and with little overhead
from flup.server.fcgi import WSGIServer
import sys, urlparse
import math, time
#This module governs the 16-channel Adafruit PWM
import Adafruit_PCA9685
import serial
pwm = Adafruit_PCA9685.PCA9685()
#300 frequency is good for driving DC motors
pwm.set_pwm_freq(300)

#pin addresses

#back left motor
m1coast   = 0
m1pwm     = 1
m1forward = 2

#back right 
m3coast   = 8
m3pwm     = 9
m3forward = 10

#front left
m2coast   = 4
m2pwm     = 5
m2forward = 6

#front right
m4coast   = 12  
m4pwm     = 13
m4forward = 14

contact = 0
servoResponse = 0
armState = 3
#ser = serial.Serial('/dev/ttyACM0', 9600, timeout=2);
#ser.write('4')
def app(environ, start_response):
	global contact
	global servoResponse
	#global ser
	global armState
	string = ""
	#parse the http request into x and y percentages
	start_response("200 OK", [("Content-Type", "text/html")])
	i = urlparse.parse_qs(environ["QUERY_STRING"])
	'''
	if contact == 0:
                if ser.readline() != "":
                        contact = 1
			string += "Found serial connection. "
		else:
			ser.write('2');
			ser.write('3');
			string += "Waiting for serial connection. "
        else:
		if "g" in i and "a" in i:
			g = i["g"][0];
			a = i["a"][0];
			# if g == "open":
			#	g = '0'
			#else:
			#	g = '1'
			if a == "open":
				a = '2'
			else:
				a = '3'
			if (a != armState):	
				# ser.write(g);
				ser.write(a);
				armState = a
	'''

	if "x" in i and "y" in i:
		x = int(i["x"][0])
		y = int(i["y"][0])
		if (abs(x) < 10 ) and (abs(y) < 10):
			pwm.set_pwm(m1pwm, 0, 0)
                        pwm.set_pwm(m3pwm, 0, 0)
                        pwm.set_pwm(m2pwm, 0, 0)
                        pwm.set_pwm(m4pwm, 0, 0)
			yield(string)
			return

		#the speed of the faster wheel
                maxSpeed = int( (math.sqrt(y**2 + x**2) * 4095) / 100 )
		baseSpeed = int (maxSpeed / 2)
		leftSpeed = baseSpeed + (x * baseSpeed / 100)
		rightSpeed = baseSpeed - (x * baseSpeed / 100)
		#the speed of the slower wheel
		maxLower = maxSpeed - int(maxSpeed * abs(x) / 100)

		#debug string for the client
		string += "x: " + str(x) + " y: " + str(y)
	        pwm.set_pwm(m1coast, 0, 4095)
                pwm.set_pwm(m3coast, 0, 4095)
                pwm.set_pwm(m2coast, 0, 4095)
                pwm.set_pwm(m4coast, 0, 4095)

		#if y is positive, set the motors to forward mode
		if y < 0:
			pwm.set_pwm(m1forward, 0, 0)
			pwm.set_pwm(m3forward, 0, 0)
                        pwm.set_pwm(m2forward, 0, 4095)
			pwm.set_pwm(m4forward, 0, 4095)

			string += " Moving forward "
		else:
			pwm.set_pwm(m1forward, 0, 4095)
			pwm.set_pwm(m3forward, 0, 4095)
			pwm.set_pwm(m2forward, 0, 0)
			pwm.set_pwm(m4forward, 0, 0)
			string += " Moving backward"
		#set the speed of each wheel according to direction
		pwm.set_pwm(m1pwm, 0, leftSpeed)
                pwm.set_pwm(m3pwm, 0, leftSpeed)
                pwm.set_pwm(m2pwm, 0, rightSpeed)
                pwm.set_pwm(m4pwm, 0, rightSpeed)

		if x >= 0:
			string += " and moving right"
		else:
			string += " and moving left"
		#return the debug string
		yield(string);
	#something went wrong. blarg!
	else:
		yield ('blargh')
#run the app!
WSGIServer(app).run()
