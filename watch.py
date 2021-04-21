from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import sys
import os
import cv2 as cv
import numpy as np
import json

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
rawCapture = PiRGBArray(camera)
time.sleep(0.2) # allow the camera to warmup

# cv.waitKey(0)



for i in range(10):
	camera.capture(rawCapture, format="bgr")
	image = rawCapture.array
	cv.imshow("Image", image)
	time.sleep(2)