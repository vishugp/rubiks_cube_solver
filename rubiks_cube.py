#!/ust/bin/env python
#rubiks_cube
#192.168.1.8:8080
from collections import deque
import urllib.request 
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time
import rospy


ap = argparse.ArgumentParser()
ap.add_argument("-b", "--buffer", type=int, default=64,help="max buffer size")
ap.add_argument('-url',"--url", action = 'store_true', help="Takes input from the IP WEBCAM")
ap.add_argument('-cam',"--cam",action = 'store_true', help = "Takes input from device camera")
ap.add_argument("-a", "--min-area", type=int, default=50, help="minimum area size")
args = vars(ap.parse_args())


if args["url"]:
    URL = input("Enter the URL of the IP camera : ")

    URLS = ''

    for i in "http://192.168.1.":
        URLS += i
    for i in URL:
        URLS += i
    for i in ":8080/shot.jpg":
        URLS += i
    print(URLS)

else:
    vs = VideoStream(0).start()
    #time.sleep(2.0)

while True:
    if(args["url"]==True):
        imgResp = urllib.request.urlopen(URLS)
        img_arr = np.array(bytearray(imgResp.read()),dtype=np.uint8)
        frame = cv2.imdecode(img_arr,1)
    else:
        frame = vs.read()
        frame=cv2.flip(frame,1)
        
    text = ""
    
    if frame is None:
        break

    hsvframe  =cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    yellow_lower = np.array([ 25, 214 ,166],np.uint8)
    yellow_upper = np.array([ 33, 255, 255],np.uint8)

    orange_lower = np.array([  0 ,203 ,175],np.uint8)
    orange_upper = np.array([ 25, 255, 227],np.uint8)

    violet_lower = np.array( [ 135  , 91,137],np.uint8)
    violet_upper = np.array([145  ,189, 187],np.uint8)

    red_lower = np.array([169  ,154, 168],np.uint8)
    red_upper = np.array([201 ,255, 255],np.uint8)

    blue_lower = np.array( [ 105 ,164, 131],np.uint8)
    blue_upper = np.array([124 ,209 ,195],np.uint8)

    green_lower = np.array([ 62 ,153, 36],np.uint8)
    green_upper = np.array( [89 ,255 ,101],np.uint8)

    yellow = cv2.inRange(hsvframe, yellow_lower, yellow_upper)
    orange = cv2.inRange(hsvframe, orange_lower, orange_upper)
    violet = cv2.inRange(hsvframe, violet_lower, violet_upper)
    red = cv2.inRange(hsvframe, red_lower, red_upper)
    blue = cv2.inRange(hsvframe, blue_lower, blue_upper)
    green = cv2.inRange(hsvframe,  green_lower, green_upper)

    kernal = np.ones((5,5),"uint8")

    yellow = cv2.dilate(yellow, kernal)
    res_yellow = cv2.bitwise_and(frame, frame,mask = yellow) 

    orange = cv2.dilate(orange, kernal)
    res_orange = cv2.bitwise_and(frame, frame,mask = orange) 

    violet = cv2.dilate(violet, kernal)
    res_violet = cv2.bitwise_and(frame, frame,mask = violet) 

    red = cv2.dilate(red, kernal)
    res_red = cv2.bitwise_and(frame, frame,mask = red) 

    blue = cv2.dilate(blue, kernal)
    res_blue = cv2.bitwise_and(frame, frame,mask = blue) 

    green = cv2.dilate(green, kernal)
    res_green = cv2.bitwise_and(frame, frame,mask = green) 
    
    contours , hierarchy = cv2.findContours(yellow, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area>1800):
            x,y,w,h = cv2.boundingRect(contour)
            #frame = cv2.rectangle(frame , (x,y) , (x+w,y+h),(0,255,255),6)
            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            frame = cv2.drawContours(frame , [box] , 0 , (0,255,255) , 9)
            xindex = int(x + w/4)
            yindex = int(y+h/1.5)
            cv2.putText(frame , "Y", (xindex,yindex) , cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,255,255))
            #cv2.putText(frame , "Color: yellow", (100,100) , cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,0,255))

    contours , hierarchy = cv2.findContours(orange, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area>1800):
            x,y,w,h = cv2.boundingRect(contour)
            #frame = cv2.rectangle(frame , (x,y) , (x+w,y+h),(0,128,255),6)
            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            frame = cv2.drawContours(frame , [box] , 0 , (0,128,255) , 9)
            xindex = int(x + w/4)
            yindex = int(y+h/1.5)
            cv2.putText(frame , "O", (xindex,yindex) , cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,255,255))
            #cv2.putText(frame , "Color: orange", (100,100) , cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,0,255))

    contours , hierarchy = cv2.findContours(violet, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area>1800):
            x,y,w,h = cv2.boundingRect(contour)
            #frame = cv2.rectangle(frame , (x,y) , (x+w,y+h),(0,0,255),6)
            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            frame = cv2.drawContours(frame , [box] , 0 , (203,192,255) , 9)
            xindex = int(x + w/4)
            yindex = int(y+h/1.5)
            cv2.putText(frame , "V", (xindex,yindex) , cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,255,255))
            #cv2.putText(frame , "Color: violet", (100,100) , cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,0,127))

    contours , hierarchy = cv2.findContours(red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area>1800):
            x,y,w,h = cv2.boundingRect(contour)
            #frame = cv2.rectangle(frame , (x,y) , (x+w,y+h),(0,0,255),6)
            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            frame = cv2.drawContours(frame , [box] , 0 , (0,0,255) , 9)
            xindex = int(x + w/4)
            yindex = int(y+h/1.5)
            cv2.putText(frame , "R", (xindex,yindex) , cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,255,255))
            #cv2.putText(frame , "Color: red", (100,100) , cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,0,255))

    contours , hierarchy = cv2.findContours(blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area>1800):
            x,y,w,h = cv2.boundingRect(contour)
            #frame = cv2.rectangle(frame , (x,y) , (x+w,y+h),(255,0,0),6)
            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            frame = cv2.drawContours(frame , [box] , 0 , (255,255,0) , 9)
            xindex = int(x + w/4)
            yindex = int(y+h/1.5)
            cv2.putText(frame , "B", (xindex,yindex) , cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,255,255))
            #cv2.putText(frame , "Color: blue", (100,100) , cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,0,255))

    contours , hierarchy = cv2.findContours(green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area>1800):
            x,y,w,h = cv2.boundingRect(contour)
            #frame = cv2.rectangle(frame , (x,y) , (x+w,y+h),(0,255,0),6)
            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            frame = cv2.drawContours(frame , [box] , 0 , (0,255,0) , 9)
            xindex = int(x + w/4)
            yindex = int(y+h/1.5)
            cv2.putText(frame , "G", (xindex,yindex) , cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,255,255))

    cv2.imshow("RUBIC'S CUBE", frame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        vs.stop()
        cv2.destroyAllWindows()
        break


