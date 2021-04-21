from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import sys
import os
import cv2 as cv
import numpy as np
import json


model = cv.CascadeClassifier('training/cascade.xml')


# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
# allow the camera to warmup
time.sleep(0.1)
# capture frames from the camera


for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	image = frame.array

	# Detection
	image = cv2.rectangle(image, (10, 10), (50, 50), (255, 0, 0), 2)
	# show the frame
	cv.imshow("Frame", image)
	key = cv.waitKey(1) & 0xFF
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break