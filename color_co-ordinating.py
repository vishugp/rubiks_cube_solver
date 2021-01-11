#!/usr/bin/env python
import cv2
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Pose
import numpy as np
import argparse
import urllib
from imutils.video import VideoStream

rospy.init_node("color_coordination")

ap = argparse.ArgumentParser()
ap.add_argument("-b", "--buffer", type=int, default=64,help="max buffer size")
ap.add_argument('-url',"--url", action = 'store_true', help="Takes input from the IP WEBCAM")
ap.add_argument('-cam',"--cam",action = 'store_true', help = "Takes input from device camera")
ap.add_argument("-a", "--min-area", type=int, default=50, help="minimum area size")
args = vars(ap.parse_args())

tab = "192.168.1.11:8080"
oneplus = "192.168.1.7:8080"
nokia = "192.168.1.6:8080"
if args["url"]:
    URL = input("Enter IP camera : ")
    URLS = ''

    for i in "http://192.168.1.":
        URLS += i
    for i in URL:
        URLS += i
    for i in ":8080/shot.jpg":
        URLS += i


# else:
#     cap = VideoStream(0).start()
    #time.sleep(2.0)

def nothing(pos):
	pass

#cap=cv2.VideoCapture(0)


def color_coordinate(colorname):
	cv2.namedWindow('Thresholds')
	cv2.createTrackbar('LH','Thresholds',0,255, nothing)
	cv2.createTrackbar('LS','Thresholds',0,255, nothing)
	cv2.createTrackbar('LV','Thresholds',0,255, nothing)
	cv2.createTrackbar('UH','Thresholds',255,255, nothing)
	cv2.createTrackbar('US','Thresholds',255,255, nothing)
	cv2.createTrackbar('UV','Thresholds',255,255, nothing)
	cv2.createTrackbar('ADD COLOUR?','Thresholds',0,1,nothing)
	cv2.createTrackbar('Finish','Thresholds',0,1,nothing)
	
	while(1):
		if(args["url"]==True):
			imgResp = urllib.request.urlopen(URLS)
			#print(type(imgResp))
			img_arr = np.array(bytearray(imgResp.read()),dtype=np.uint8)
			#print(img_arr)
			frame = cv2.imdecode(img_arr,1)
		else:
			cap = VideoStream(0).start()
			frame = cap.read()
			frame=cv2.flip(frame,1)
		text = ""

		if frame is None:
			break

		# _, img = cap.read()
		# img=cv2.flip(img,1)  

		#img = imutils.resize(frame, width=1250)
			
		#converting frame (img i.e BGR) to HSV (hue-saturation-value)
		hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
		
		lh=cv2.getTrackbarPos('LH','Thresholds')
		ls=cv2.getTrackbarPos('LS','Thresholds')
		lv=cv2.getTrackbarPos('LV','Thresholds')

		uh=cv2.getTrackbarPos('UH','Thresholds')
		us=cv2.getTrackbarPos('US','Thresholds')
		uv=cv2.getTrackbarPos('UV','Thresholds')

		add=cv2.getTrackbarPos('ADD COLOUR?','Thresholds')
		end=cv2.getTrackbarPos('Finish','Thresholds')

		#Defining the Range of color
		color_lower=np.array([lh,ls,lv],np.uint8)
		color_upper=np.array([uh,us,uv],np.uint8)
		
		
		#Finding the range of color in the image

		color=cv2.inRange(hsv,color_lower,color_upper)
		
		#Morphological transformation, Dilation  	
		kernal = np.ones((5 ,5), "uint8")
		color=cv2.dilate(color,kernal)
		cv2.imshow("Color Transformation",color)
		cv2.imshow("Original Image",frame)	
		if add == 1:
			#vs.stop()
			cv2.destroyAllWindows()
			print(colorname)
			print("LowerHSV: ",color_lower)
			print("UpperHSV: ",color_upper)
			colorname=input("Enter Next color: ")
			color_coordinate(colorname)
			
			
		if end == 1:
			print(colorname)
			print("LowerHSV: ",color_lower)
			print("UpperHSV: ",color_upper)
			break
		if cv2.waitKey(1)== ord('q'):
			print(colorname)
			print("LowerHSV: ",color_lower)
			print("UpperHSV: ",color_upper)
			break
	#cap.release()
	vs.stop()
	cv2.destroyAllWindows()

if __name__ == "__main__":
	colornaav = input("Enter Color Name: ")
	color_coordinate(colornaav)