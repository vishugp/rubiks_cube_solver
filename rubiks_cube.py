#!/ust/bin/env python
#rubiks_cube
#192.168.1.8:8080
from collections import deque
from operator import itemgetter
import urllib.request 
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time
import rospy
import kociemba



ap = argparse.ArgumentParser()
ap.add_argument("-b", "--buffer", type=int, default=64,help="max buffer size")
ap.add_argument('-url',"--url", action = 'store_true', help="Takes input from the IP WEBCAM")
ap.add_argument('-cam',"--cam",action = 'store_true', help = "Takes input from device camera")
ap.add_argument("-a", "--min-area", type=int, default=50, help="minimum area size")
args = vars(ap.parse_args())

face = []
faces = []
instr = [0,0,0,0,0,0]
countlol = 0
setup=''
ksetup=''

if args["url"]:
    URL = input("Enter the URL of the IP camera : ")

    URLS = ''

    for i in "http://192.168.43.121":
        URLS += i
    for i in URL:
        URLS += i
    for i in ":8080/shot.jpg":
        URLS += i
    print(URLS)

else:
    vs = VideoStream(0).start()
    #time.sleep(2.0)
def nothing(pos):
	pass

cv2.namedWindow('Instructions',cv2.WINDOW_NORMAL)

cv2.createTrackbar('Front','Instructions',0,3,nothing)
cv2.createTrackbar('Down','Instructions',0,3,nothing)
cv2.createTrackbar('Left','Instructions',0,3,nothing)
cv2.createTrackbar('Up','Instructions',0,3,nothing)
cv2.createTrackbar('Right','Instructions',0,3,nothing)
cv2.createTrackbar('Back','Instructions',0,3,nothing)


while True:
    if(args["url"]==True):
        imgResp = urllib.request.urlopen(URLS)
        img_arr = np.array(bytearray(imgResp.read()),dtype=np.uint8)
        frame = cv2.imdecode(img_arr,1)
    else:
        frame = vs.read()        
        frame=cv2.flip(frame,1)
    
    instr[0] =cv2.getTrackbarPos('Front','Instructions')
    instr[1] =cv2.getTrackbarPos('Down','Instructions')
    instr[2] =cv2.getTrackbarPos('Left','Instructions')
    instr[3] =cv2.getTrackbarPos('Up','Instructions')
    instr[4] =cv2.getTrackbarPos('Right','Instructions')
    instr[5] =cv2.getTrackbarPos('Back','Instructions')
    
    stored = [
                [20, 90], [37, 90], [54, 90],
                [20, 107], [37, 107], [54, 107],
                [20, 124], [37, 124], [54, 124]
        ]
    
    preview = [
                [120, 390], [165, 390], [210, 390],
                [120, 435], [165, 435], [210, 435],
                [120, 480], [165, 480], [210, 480]
        ]
    colorpalette = {

        'Y': (0,255,255) ,
        'O': (0,128,255) ,
        'V': (203,192,255),
        'R': (0,0,255) ,
        'B': (255,255,0),
        'G': (0,255,0)

    }

    shift = {

        'front' : (54,0),
        'up' : (54,-54),
        'down' : (54,54),
        'left' : (0,0),
        'right' : (108,0),
        'back' : (162,0)
    }
    
    if frame is None:
        break

    vertices = []
    count = 0

    # for (x,y) in stored:
        #cv2.rectangle( frame, (x,y), (x+15,y+15),(0,0,0))
        #v2.rectangle( frame, (x +54,y+54), (x+15+54,y+15+54),(0,0,0))
        #cv2.rectangle( frame, (x +54,y), (x+15+54,y+15),(0,0,0),-1)
        #cv2.rectangle( frame, (x +54,y-54), (x+15+54,y+15-54),(0,0,0))
        #cv2.rectangle( frame, (x +54+54,y), (x+15+54+54,y+15),(0,0,0))
        #cv2.rectangle( frame, (x +54+54+54,y), (x+15+54+54+54,y+15),(0,0,0))

    frame = imutils.resize(frame, width=1250)
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
            vertices.append((xindex,yindex,'Y'))
            count+=1
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
            vertices.append((xindex,yindex,'O'))
            count+=1
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
            vertices.append((xindex,yindex,'V'))
            count+=1
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
            vertices.append((xindex,yindex,'R'))
            count+=1
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
            vertices.append((xindex,yindex,'B'))
            count+=1
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
            vertices.append((xindex,yindex,'G'))
            count+=1
            cv2.putText(frame , "G", (xindex,yindex) , cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,255,255))

    cv2.imshow("RUBIC'S CUBE", frame)


    #if cv2.waitKey(10) & 0xFF == ord('p'):
    if count == 9:
        vertices.sort(key=lambda x: x[1])

        for i in [0,3,6]:
            row = vertices[i:i+3]
            row.sort(key = lambda x :x[0])
            for j in row:
                face.append(j[2])
        #print(face)
        #print(face)
        for i in range (len(face)):
            (x,y) = preview[i]
            #print(x,y)
            cv2.rectangle(frame, (x,y), (x+40,y+40),colorpalette[face[i]] , -1)
            #cv2.rectangle( frame, (x-3,y-3), (x+26,y+26),(0,0,0))
            #cv2.imshow("RUBIC'S CUBE", frame)
                # cv2.rectangle( frame, (x +54,y+54), (x+15+54,y+15+54),colorpalette[i] , -1)
                # cv2.rectangle( frame, (x ,y), (x+15,y+15),colorpalette[i] , -1)
                # cv2.rectangle( frame, (x +54,y-54), (x+15+54,y+15-54),colorpalette[i] , -1)
                # cv2.rectangle( frame, (x +54+54,y), (x+15+54+54,y+15),colorpalette[i] , -1)
                # cv2.rectangle( frame, (x +54+54+54,y), (x+15+54+54+54,y+15),colorpalette[i] , -1)
        thickness = 3
        cv2.putText(frame,"PREVIEW", (x-90,y+70),cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,0,0),thickness)

        if instr[0] > 0 :
            if instr[0] ==1:
                for fi in range (len(face)):
                    (a,b) = stored[fi]
                    (sa,sb)=shift['front']
                    cv2.rectangle(frame, (a+sa,b+sb), (a+sa+15,b+sb+15),colorpalette[face[fi]] , -1)
                    cv2.putText(frame,"FRONT: Sure Ah?", (x-90,y+100),cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,0,0),thickness)
            if instr[0] ==2:
                instr[0]=3
                frontside = face
                cv2.setTrackbarPos('Front','Instructions',3)


        if instr[1] > 0 :
            if instr[1] ==1:
                for fi in range (len(face)):
                    (a,b) = stored[fi]
                    (sa,sb)=shift['down']
                    cv2.rectangle(frame, (a+sa,b+sb), (a+sa+15,b+sb+15),colorpalette[face[fi]] , -1)
                    cv2.putText(frame,"DOWN: Sure Ah?", (x-90,y+100),cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,0,0),thickness)
            if instr[1] ==2:
                instr[1]=3
                downside = face
                cv2.setTrackbarPos('Down','Instructions',3)

            


        if instr[2] > 0 :
            if instr[2] == 1:
                for fi in range (len(face)):
                    (a,b) = stored[fi]
                    (sa,sb)=shift['left']
                    cv2.rectangle(frame, (a+sa,b+sb), (a+sa+15,b+sb+15),colorpalette[face[fi]] , -1)
                    cv2.putText(frame,"LEFT: Sure Ah?", (x-90,y+100),cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,0,0),thickness)
            if instr[2] ==2:
                instr[2]=3
                leftside = face
                cv2.setTrackbarPos('Left','Instructions',3)

            


        if instr[3] > 0 :
            if instr[3] ==1:
                for fi in range (len(face)):
                    (a,b) = stored[fi]
                    (sa,sb)=shift['up']
                    cv2.rectangle(frame, (a+sa,b+sb), (a+sa+15,b+sb+15),colorpalette[face[fi]] , -1)
                    cv2.putText(frame,"UP: Sure Ah?", (x-90,y+100),cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,0,0),thickness)
            if instr[3] ==2:
                instr[3]=3 
                upside = face
                cv2.setTrackbarPos('Up','Instructions',3)

            


        if instr[4] > 0 :
            if instr[4] ==1:
                for fi in range (len(face)):
                    (a,b) = stored[fi]
                    (sa,sb)=shift['right']
                    cv2.rectangle(frame, (a+sa,b+sb), (a+sa+15,b+sb+15),colorpalette[face[fi]] , -1)
                    cv2.putText(frame,"RIGHT: Sure Ah?", (x-90,y+100),cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,0,0),thickness)
            if instr[4] ==2:
                instr[4]=3
                rightside = face
                cv2.setTrackbarPos('Right','Instructions',3)

            


        if instr[5] > 0 :
            if instr[5] ==1:
                for fi in range (len(face)):
                    (a,b) = stored[fi]
                    (sa,sb)=shift['back']
                    cv2.rectangle(frame, (a+sa,b+sb), (a+sa+15,b+sb+15),colorpalette[face[fi]] , -1)
                    cv2.putText(frame,"BACK: Sure Ah?", (x-90,y+100),cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,0,0),thickness)
            if instr[5] ==2:
                instr[5]=3
                backside = face
                cv2.setTrackbarPos('Back','Instructions',3)

           



    if instr[0] ==3:
        for fi in range (len(frontside)):
            (a,b) = stored[fi]
            (sa,sb)=shift['front']
            cv2.rectangle(frame, (a+sa,b+sb), (a+sa+15,b+sb+15),colorpalette[frontside[fi]] , -1)

    if instr[1] ==3:
        for fi in range (len(downside)):
            (a,b) = stored[fi]
            (sa,sb)=shift['down']
            cv2.rectangle(frame, (a+sa,b+sb), (a+sa+15,b+sb+15),colorpalette[downside[fi]] , -1)

    if instr[2] ==3:
        for fi in range (len(leftside)):
            (a,b) = stored[fi]
            (sa,sb)=shift['left']
            cv2.rectangle(frame, (a+sa,b+sb), (a+sa+15,b+sb+15),colorpalette[leftside[fi]] , -1)

    if instr[3] ==3:
        for fi in range (len(upside)):
            (a,b) = stored[fi]
            (sa,sb)=shift['up']
            cv2.rectangle(frame, (a+sa,b+sb), (a+sa+15,b+sb+15),colorpalette[upside[fi]] , -1)

    if instr[4] ==3:
        for fi in range (len(rightside)):
            (a,b) = stored[fi]
            (sa,sb)=shift['right']
            cv2.rectangle(frame, (a+sa,b+sb), (a+sa+15,b+sb+15),colorpalette[rightside[fi]] , -1)

    if instr[5] ==3:
        for fi in range (len(backside)):
            (a,b) = stored[fi]
            (sa,sb)=shift['back']
            cv2.rectangle(frame, (a+sa,b+sb), (a+sa+15,b+sb+15),colorpalette[backside[fi]] , -1)


    face=[]
   
    if instr == [3,3,3,3,3,3] and countlol == 0:
        for i in upside:
            faces.append(i)
        for i in rightside:
            faces.append(i)
        for i in frontside:
            faces.append(i)
        for i in downside:
            faces.append(i)
        for i in leftside:
            faces.append(i)
        for i in backside:
            faces.append(i)
        print("MAST")
        countlol =1



    cv2.imshow("RUBIC'S CUBE", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        #print(len(faces))
        #print(faces)
        for s in faces:
            setup += s
        print(setup)
        for m in range (len(setup)):
            if setup[m]=='V':
                ksetup+='U'
            if setup[m]=='O':
                ksetup+='F'
            if setup[m]=='Y':
                ksetup+='D'
            if setup[m]=='B':
                ksetup+='L'
            if setup[m]=='G':
                ksetup+='R'
            if setup[m]=='R':
                ksetup+='B'
        print(ksetup)                                
        answer = kociemba.solve(ksetup)
        print("#####################  ANSWER  ####################")
        print(answer)
        cv2.destroyAllWindows()
        vs.stop()
        break


