# USAGE
# python object_movement.py --video object_tracking_example.mp4
# python object_movement.py

# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import thread

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=32,
	help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space
# default for green was lower (29,86,6)   upper (64,255,255)
greenLower = (40, 86, 125)
greenUpper = (70, 255, 255)

redLower =(165,60,50)
redUpper = (180,255,255)

blueLower =(96,60,50)
blueUpper = (134,255,255)


# initialize the list of tracked points, the frame counter,
# and the coordinate deltas
pts = deque(maxlen=args["buffer"])
counter = 0
(dX, dY) = (0, 0)
direction = ""

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
	camera = cv2.VideoCapture(0)

# otherwise, grab a reference to the video file
else:
	camera = cv2.VideoCapture(args["video"])

def green():
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask_g = cv2.inRange(hsv, greenLower, greenUpper)
	mask_g = cv2.erode(mask_g, None, iterations=2)
	mask_g = cv2.dilate(mask_g, None, iterations=2)
	cnts = cv2.findContours(mask_g.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None
	if len(cnts) > 0:
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		if radius > 10:
                        cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 0), 2)
def red():
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask_r = cv2.inRange(hsv, redLower, redUpper)
	mask_r = cv2.erode(mask_r, None, iterations=2)
	mask_r = cv2.dilate(mask_r, None, iterations=2)
	cnts = cv2.findContours(mask_r.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None
	if len(cnts) > 0:
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		if radius > 10:
                        cv2.circle(frame, (int(x), int(y)), int(radius),(0, 0, 255), 2)

def blue():
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask_b = cv2.inRange(hsv, blueLower, blueUpper)
	mask_b = cv2.erode(mask_b, None, iterations=2)
	mask_b = cv2.dilate(mask_b, None, iterations=2)
	cnts = cv2.findContours(mask_b.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None
	if len(cnts) > 0:
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		if radius > 10:
                        cv2.circle(frame, (int(x), int(y)), int(radius),(255, 0, 0), 2)


# keep looping
while True:
	(grabbed, frame) = camera.read()
	if args.get("video") and not grabbed:
		break
	frame = imutils.resize(frame, width=600)
        
        try:
            thread.start_new_thread(green,(""))
            thread.start_new_thread(red,(""))
            thread.start_new_thread(blue,(""))
        except:
            print "Error Starting thread"
                        
	# show the frame to our screen and increment the frame counter
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	counter += 1

        #if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
