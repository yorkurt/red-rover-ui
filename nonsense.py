from math import atan, degrees, sqrt
rover-width = 100
rover-length = 100
while True:	
	input = raw_input("Please enter the values for x and y with ',' in between")
	input = input.split(,)
	x = int(input[0])
	y = int(input[1])
	string = "x: " + str(x) + " y: " + str(y)
	theta = int(degrees(atan(float(y)/float(x))))
	radius = sqrt(x**2 + y**2)
	if y >= 0:
		string += " Moving forward "
	else:
		string += " Moving backward"
	if not(abs(theta)>=80 or abs(theta)<=10):
		
	string += "at a relative speed of " + str(float(r)/100) + " percent"
	print(string)
