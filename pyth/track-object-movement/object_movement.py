# USAGE
# python object_movement.py --video object_tracking_example.mp4
# python object_movement.py

# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import sys
import time
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

blueLower =(90,20,0)
blueUpper = (140,255,255)

whiteLower =(0,225,50)
whiteUpper =(180,255,255)

font=cv2.FONT_HERSHEY_SIMPLEX

imsize=300

cv2.namedWindow('White1')
cv2.moveWindow('White1',0,100)

cv2.namedWindow('White2')
cv2.moveWindow('White2',imsize,100)

cv2.namedWindow('White3')
cv2.moveWindow('White3',0,100+imsize)

cv2.namedWindow('Output')
cv2.moveWindow('Output',imsize,100+imsize)


# initialize the list of tracked points, the frame counter,
# and the coordinate deltas
pts = deque(maxlen=args["buffer"])
counter = 0
(dX, dY) = (0, 0)
direction = ""
x1=0
x2=imsize
y1=0
y2=imsize
# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
	camera = cv2.VideoCapture(0)

# otherwise, grab a reference to the video file
else:
	camera = cv2.VideoCapture(args["video"])
time.sleep(2)
# keep looping


#Resize on board


(grabbed, frame) = camera.read()
    

# resize the frame, blur it, and convert it to the HSV
# color space
frame = imutils.resize(frame, width=imsize)
#img[y1:y2,x1:x2]
frame=frame[y1:y2,x1:x2]
# blurred = cv2.GaussianBlur(frame, (11, 11), 0)
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

mask_b = cv2.inRange(hsv, blueLower, blueUpper)
#cv2.imshow("Blue1", mask_b)
mask_b = cv2.erode(mask_b, None, iterations=1)
#cv2.imshow("Blue2", mask_b)
mask_b = cv2.dilate(mask_b, None, iterations=8)
#cv2.imshow("Blue3", mask_b)
# find contours in the mask and initialize the current
# (x, y) center of the ball
cnts = cv2.findContours(mask_b.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)[-2]
center = None

# only proceed if at least one contour was found
if len(cnts) > 0:
    # find the largest contour in the mask, then use
    # it to compute the minimum enclosing circle and
    # centroid
    c = max(cnts, key=cv2.contourArea)
    ((x, y), radius) = cv2.minEnclosingCircle(c)
    M = cv2.moments(c)
    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
    
    # only proceed if the radius meets a minimum size (default was 10)
    if radius > 20:
        # draw the circle and centroid on the frame,
        # then update the list of tracked points
        #first color is 0,255,255
                    #print "Blue!"
                    x=int(x)
                    y=int(y)
                    radius=int(radius)
                    cv2.circle(mask_b, (x, y), radius,(255, 0, 0), 2)
                    #cv2.imshow("Blue3",mask_b)
                    x1=x-radius
                    x2=x+(radius)
                    y1=y-radius
                    y2=y+radius
                    print("X1:",x1," X2:",x2," Y1:",y1," Y2:",y2)
#End of board sizing
exit


while True:
    # grab the current frame
    (grabbed, frame) = camera.read()
    
    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if args.get("video") and not grabbed:
        break

    # resize the frame, blur it, and convert it to the HSV
    # color space
    frame = imutils.resize(frame, width=imsize)
    #img[y1:y2,x1:x2]
    frame=frame[y1:y2,x1:x2]
    # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask_w = cv2.inRange(hsv, whiteLower, whiteUpper)
    cv2.imshow("White1", mask_w)
    #mask_w = cv2.erode(mask_w, None, iterations=2)
    cv2.imshow("White2", mask_w)
    mask_w = cv2.dilate(mask_w, None, iterations=2)
    cv2.imshow("White3", mask_w)
    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask_w.copy(),
                            cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
    fishcount=0
    # only proceed if at least one contour was found
    if len(cnts) > 0:
        for c in range(0,len(cnts)):
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            #c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(cnts[c])
            M = cv2.moments(cnts[c])
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            # only proceed if the radius meets a minimum size (default was 10)
            #print ("Radius:",radius)
            if radius > 9 and radius <13:
                    fishcount=fishcount+1
                    # draw the circle and centroid on the frame,
                    # then update the list of tracked points
                    #first color is 0,255,255
                    #print "Green"
                    cv2.circle(frame, (int(x), int(y)), int(radius),(0, 0, 0), 2)
            #fishtext=str(fishcount)
            #cv2.putText(frame,fishtext,(10,20),font,1,(255,255,255),1)
            print("Fish COunt: ",fishcount)
#End of White
##    mask_r = cv2.inRange(hsv, redLower, redUpper)
##    mask_r = cv2.erode(mask_r, None, iterations=2)
##    mask_r = cv2.dilate(mask_r, None, iterations=2)
##
##    # find contours in the mask and initialize the current
##    # (x, y) center of the ball
##    cnts = cv2.findContours(mask_r.copy(), cv2.RETR_EXTERNAL,
##            cv2.CHAIN_APPROX_SIMPLE)[-2]
##    center = None
##
##    # only proceed if at least one contour was found
##    if len(cnts) > 0:
##            # find the largest contour in the mask, then use
##            # it to compute the minimum enclosing circle and
##            # centroid
##            c = max(cnts, key=cv2.contourArea)
##            ((x, y), radius) = cv2.minEnclosingCircle(c)
##            M = cv2.moments(c)
##            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
##
##            # only proceed if the radius meets a minimum size (default was 10)
##            if radius > 5:
##                    # draw the circle and centroid on the frame,
##                    # then update the list of tracked points
##                    #first color is 0,255,255
##                    #print "Red"
##                    cv2.circle(frame, (int(x), int(y)), int(radius),(0, 0, 255), 2)
#End of red

    


    # show the frame to our screen and increment the frame counter
    frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    cv2.imshow("Output", frame)
    key = cv2.waitKey(1) & 0xFF
    counter += 1
    #if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
