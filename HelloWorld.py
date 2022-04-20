
import mraa
import time
import sys
import cv2
import numpy as np
from matplotlib import pyplot as plt
import zmq
import base64




# GPIO
pin = 18
pin2 = 35
pin3 = 19
pin4 = 33
pin5 = 21
pin6 = 24

servoOnePin = 11
servoTwoPin = 13

# initialise GPIO take picture
takePic = mraa.Gpio(pin)
takePic.dir(mraa.DIR_IN)

panLeft = mraa.Gpio(pin2)
panLeft.dir(mraa.DIR_IN)

panRight = mraa.Gpio(pin3)
panRight.dir(mraa.DIR_IN)

tiltUp = mraa.Gpio(pin4)
tiltUp.dir(mraa.DIR_IN)

tiltDown = mraa.Gpio(pin5)
tiltDown.dir(mraa.DIR_IN)

hostControl = mraa.Gpio(pin6)
hostControl.dir(mraa.DIR_IN)

#pan servo gpio
servoPan = mraa.Pwm(servoOnePin)
servoPan.period_ms(20)
servoPan.enable(True)
#pan servo gpio
servoTilt = mraa.Pwm(servoTwoPin)
servoTilt.period_ms(20)
servoTilt.enable(True)

value= 0.075
tiltValue = 0.06

def takePicandDisplayRemote():
    # thank you! https://stackoverflow.com/questions/24791633/zeromq-pyzmq-send-jpeg-image-over-tcp
	cam = cv.VideoCapture(4)
    # cv.namedWindow("CSE398")

	img_counter = 0
	ret, frame = cam.read()
	if not ret:
		print("failed to grab frame")

	img_name = "opencv_frame_{}.png".format(img_counter)
	cv.imwrite(img_name, frame)
	print("{} written!".format(img_name))
	img_counter += 1

	f = open(img_name, 'rb')
	bytes = bytearray(f.read())
	strng = base64.b64encode(bytes)
	f.close()

	return strng

while(True):
	picState = takePic.read()
	panLeftState = panLeft.read()
	panRightState = panRight.read()

	tiltUpState = tiltUp.read()

	tiltDownState = tiltDown.read()
	hostControlState = hostControl.read()
	servoPan.write(1-value)
	servoTilt.write(1-tiltValue)
	time.sleep(0.05)
	if picState == 1:
		print("takePic state was " + str(picState))
		vid = cv2.VideoCapture(4)
		result, image = vid.read()
		grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		if result:
			cv2.imshow("This a pic", grayImage)
			cv2.imwrite("TestPic.png", grayImage)
			cv2.waitKey(0)
			cv2.destroyAllWindows()
		while(picState == 1):
			picState = takePic.read()
			vid.release()
	if panLeftState == 1:
		print("panleft state was " + str(panLeftState))
		value = value - 0.005
		if value <= 0.025:
			value = 0.025
		while(panLeftState == 1):
			panLeftState = panLeft.read()
	if panRightState == 1:
		print("panRight state was " + str(panRightState))
		value = value + 0.005
		if value >= 0.125:
			value = 0.125
		while(panRightState == 1):
			panRightState = panRight.read()
	if tiltUpState == 1:
		print("tiltUpState was " + str(tiltUpState))
		tiltValue = tiltValue - 0.005
		if tiltValue <= 0.025:
			tiltValue = 0.025
		while(tiltUpState == 1):
			tiltUpState = tiltUp.read()
	if tiltDownState == 1:
		print("tiltDown state was " + str(tiltDownState))
		
		tiltValue = tiltValue + 0.005
		if tiltValue >= 0.125:
			tiltValue = 0.125
		while(tiltDownState == 1):
			tiltDownState = tiltDown.read()
	if hostControlState == 4: # identify shapes
		print("hostControl state was " + str(hostControlState))
		
		vid = cv2.VideoCapture(4)
		result, img = vid.read()
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		#gray = cv2.GaussianBlur(gray,(5,5),0)
		scalePercent = 60
		width = int(gray.shape[1])
		height = int(gray.shape[0])
		print("w:" + str(width) + " h: "+ str(height))
		#gray = cv2.resize(gray, dim, interpolation = cv2.INTER_AREA)
		# setting threshold of gray image
		ret, threshold = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)
  
		# using a findContours() function
		_,contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		  
		i = 0
		  
		# list for storing names of shapes
		for contour in contours:
		  
		    # here we are ignoring first counter because 
		    # findcontour function detects whole image as shape
			if i == 0:
				i = 1
				continue
		  
		    # cv2.approxPloyDP() function to approximate the shape
			approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
		      
		    # using drawContours() function
			cv2.drawContours(gray, [contour], 0, (0, 0, 255), 5)
		  
		    # finding center point of shape
			M = cv2.moments(contour)
			if M['m00'] != 0.0:
				x = int(M['m10']/M['m00'])
				y = int(M['m01']/M['m00'])
		  
		    # putting shape name at center of each shape
			if len(approx) == 3:
				cv2.putText(gray, 'Triangle', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
				print("Triangle (x,y): " + str(x) + "," + str(y))
		  
			elif len(approx) == 4:
				cv2.putText(gray, 'Square', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
				print("Square (x,y): " + str(x) + "," + str(y))
		
			else: #circle
				cv2.putText(gray, 'Circle', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
				print("Circle (x,y): " + str(x) + "," + str(y))
		# displaying the image after drawing contours
		cv2.imshow('shapes', gray)
		  
		cv2.waitKey(0)
		cv2.destroyAllWindows()

		while(hostControlState == 1):
			hostControlState = hostControl.read()
			vid.release()
	if hostControlState == 1:
		print("hostControl state was " + str(hostControlState))

		context = zmq.Context()
		socket = context.socket(zmq.REP)
		socket.bind('tcp://*:7000')
		while True:

        # check if there is a received packet
        # if there is a packet received, print it and do something else
			try:
				message = socket.recv()
				# print('type message is:', type(message))
				print('message recieved', message)
				message = message.decode("utf-8")
				print(message.lower())
				if message.lower() == 'getimage':
                # get image
					response = takePicandDisplayRemote()
					socket.send(response)
                # print('Called getimage method on server!')
                # socket.send(b'getimage done!')

			except zmq.Again as e:
				print('no message yet')
				
				
				
		while(hostControlState == 1):
			hostControlState = hostControl.read()
	if hostControlState == 6:
		
            
		counter = 0
		vid = cv2.VideoCapture(4)
		while(counter <  300):
			result, img = vid.read()
			gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
			vertStart = (320,0)
			vertEnd = (320,480)
			horStart = (0,240)
			horEnd = (640,240)
			color = (0,0,0)
			
			# setting threshold of gray image
			ret, threshold = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)
  
			# using a findContours() function
			_,contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		  
			i = 0
			x = 320
			y = 240
			# list for storing names of shapes
			for contour in contours:
		  
				# here we are ignoring first counter because 
				# findcontour function detects whole image as shape
				if i == 0:
					i = 1
					continue
		  
				# cv2.approxPloyDP() function to approximate the shape
				approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
			      
				# using drawContours() function
				cv2.drawContours(gray, [contour], 0, (0, 0, 255), 5)
			  
				# finding center point of shape
				M = cv2.moments(contour)
				if M['m00'] != 0.0:
					x = int(M['m10']/M['m00'])
					y = int(M['m01']/M['m00'])
			  
				# putting shape name at center of each shape
				if len(approx) == 3:
					cv2.putText(gray, 'Triangle', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
					print("Triangle (x,y): " + str(x) + "," + str(y))
			  
				elif len(approx) == 4:
					cv2.putText(gray, 'Square', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
					print("Square (x,y): " + str(x) + "," + str(y))
			
				else: #circle
					cv2.putText(gray, 'Circle', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
					print("Circle (x,y): " + str(x) + "," + str(y))
		  
			#displaying the image after drawing contours
			cv2.line(gray, vertStart, vertEnd, color, 3)
			cv2.line(gray, horStart, horEnd, color, 3)
			cv2.imshow('shapes', gray)
			if cv2.waitKey(1) & 0xFF == ord('q'):
        			break
			#time.sleep(1)
			counter+=1
			xDiff = abs(x-320)
			yDiff = abs(y-240)
			if xDiff == 0:
				xMagnitude = 0
			elif xDiff < 5:
				xMagnitude = 0.00001
			elif xDiff < 10:
				xMagnitude = 0.00005
			elif xDiff < 25:
				xMagnitude = 0.0001
			elif xDiff < 50:
				xMagnitude = 0.0002
			else:
				xMagnitude = 0.0005
			
			if yDiff == 0:
				yMagnitude = 0
			elif yDiff < 5:
				yMagnitude = 0.00001
			elif yDiff < 10:
				yMagnitude = 0.00005
			elif yDiff < 25:
				yMagnitude = 0.0001
			elif yDiff < 50:
				yMagnitude = 0.0002
			else:
				yMagnitude = 0.0005

			if x > 320:
				value = value - xMagnitude
				if value <= 0.025:
					value = 0.025
			if x <= 320:
				value = value + xMagnitude
				if value >= 0.125:
					value = 0.125
			if y < 240:
				tiltValue = tiltValue - yMagnitude
				if tiltValue <= 0.025:
					tiltValue = 0.025
			if y >= 240:
				tiltValue = tiltValue + yMagnitude
				if tiltValue >= 0.125:
					tiltValue = 0.125

			servoPan.write(1-value)
			servoTilt.write(1-tiltValue)
		vid.release()
		cv2.imshow('shapes', gray)
		cv2.waitKey(0)
		cv2.destroyAllWindows()

		while(hostControlState == 1):
			hostControlState = hostControl.read()
			vid.release()

