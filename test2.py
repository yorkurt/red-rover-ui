#!/usr/bin/pythonRoot

from flup.server.fcgi import WSGIServer
import sys, urlparse
import Adafruit_PCA9685
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(300)


def app(environ, start_response):
	pwm.set_pwm(13, 0, 2000)
	pwm.set_pwm(9, 0, 2000)
	start_response("200 OK", [("Content-Type", "text/html")])
	i = urlparse.parse_qs(environ["QUERY_STRING"])
	if "x" in i and "y" in i:
		x = int(i["x"][0])
		y = int(i["y"][0])
		string = "x: " + str(x) + " y: " + str(y)

		if y >= 0:
			pwm.set_pwm(14, 0, 0)
                        pwm.set_pwm(11, 0, 0)
			string += " Moving forward "
		else:
			pwm.set_pwm(14, 0, 4095)
			pwm.set_pwm(11, 0, 4095)
			string += " Moving backward"
		if x >= 0:
			pwm.set_pwm(15, 0, 0)
                	pwm.set_pwm(10, 0, 4095)
			string += " and moving right"
		else:
			pwm.set_pwm(15, 0, 4095)
                        pwm.set_pwm(10, 0, 0)
			string += " and moving left"
		yield(string);
	else:
		yield ('blargh')

WSGIServer(app).run()
