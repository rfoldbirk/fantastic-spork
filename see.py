import sys
import os
import cv2 as cv
import numpy as np
import json

# Globale variabler
global average_confidence
global image_path

if len(sys.argv) <= 1:
	print('Forkerte argumenter!\nArgumenter: path_to_image <average_confidence>')
	exit()

if len(sys.argv) >= 2:
	image_path = sys.argv[1]

if len(sys.argv) >= 3:
	average_confidence = int(sys.argv[2])
else:
	average_confidence = False

# Funktionen jd, eksisterer da vi har brug for at konvertere et ndArray til json ret tit.
def jd(arr):
	return json.dumps( arr.tolist() )

# findAvgBest returnerer alle rektangler som har en confidence score som er højere end gennemsnittet
# dog kan gennemsnittet overskrives når man kører programmet via andet argument
def findAvgBest(detected):
	# Beregner gennemsnittet
	avg = 0
	for score in detected[1]:
		avg += int( score[0] )
	avg = avg / len(detected[1])

	# Overskriver gennemsnittet hvis det er specificeret
	if average_confidence:
		avg = average_confidence
	
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



model = 'training/cascade.xml'
image = cv.imread(sys.argv[1])

# load the trained model
model5 = cv.CascadeClassifier('training/cascade.xml')
model10 = cv.CascadeClassifier('training/cascade.xml')

d5 = model5.detectMultiScale2(image)
d10 = model10.detectMultiScale2(image)

print(findAvgBest(d5))