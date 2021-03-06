from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import sys
import os
import cv2
import numpy as np
import json

average_confidence = False


model = cv2.CascadeClassifier('training/cascade.xml')


def jd(arr):
	return json.dumps( arr.tolist() )

def findAvgBest(detected):
	# Beregner gennemsnittet
	avg = 0
	for score in detected[1]:
		avg += int( score[0] )

	if not len(detected[1]) == 0:
		avg = avg / len(detected[1])

	# Overskriver gennemsnittet hvis det er specificeret
	if average_confidence:
		avg = average_confidence

	if avg < 15: avg = 1000
	
	# Vælger 
	selected_indexes = []
	index = 0
	for score in detected[1]:
		if int( score[0] ) > avg:
			selected_indexes.append(index)

		index += 1

	selected_rects = []
	for i in selected_indexes:
		selected_rects.append({
			"rect": jd( detected[0][i] ),
			"confidence": jd( detected[1][i][0] )
		})

	return selected_rects

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
	dms = model.detectMultiScale2(image)

	for elem in findAvgBest(dms):
		_dict = json.loads( elem["rect"] )
		score = json.loads( elem["confidence"] )

		if int(score) > 500:
			bp = (_dict[0], _dict[1])
			ep = (_dict[2], _dict[3])
			image = cv2.rectangle(image, bp, ep, (255, 0, 0), 2)
	

	# show the frame
	cv2.imshow("Frame", image)
	key = cv2.waitKey(1) & 0xFF
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break