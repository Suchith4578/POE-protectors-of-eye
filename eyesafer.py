import cv2 #cv2 is used to access
import cvzone #cvzone is used fro detecting faces and hands
import sys#sys is used to close python files(here)
from cvzone.FaceMeshModule import FaceMeshDetector #face mesh detector to detect landmarks on face
from cvzone.HandTrackingModule import HandDetector#Hand Detector to detect landmarks on Hand
import mediapipe as mp
import numpy as np
import copy
import math
cap = cv2.VideoCapture(0)#Capturing the video
detector = FaceMeshDetector(maxFaces=1)#Detecting landmarks on face

detector2=HandDetector(detectionCon=0.8,maxHands=2)#Detecting Landmarks on hand
while True:
    cap.set(3, 1280)#height of the window
    cap.set(4, 720)#length of the window
    success, img = cap.read()#taking the data from camer
    img, faces = detector.findFaceMesh(img, draw=False)
    hands,img=detector2.findHands(img,draw=True)

    if faces:#if faces are dtected
        face = faces[0]#1st face
        pointLeft = face[145]#eyeball's landmarks
        pointRight = face[374]#eyeball's landmarks
        w, _ = detector.findDistance(pointLeft, pointRight)#finds the distance between the eyeballs
        W = 6.3#average width of the face of an human

        # Finding distance
        f = 600#focal length
        d = (W * f) / w #distance
        cvzone.putTextRect(img,'Click Esc,Q or make a cross symbol to exit',(10,30),scale=1.5)#puts a rectangle and text on the top right of the window
        if d>=40 and d<=100:#if face is within 40 and 100cm
            cvzone.putTextRect(img, 'You are at a correct position',
                        (face[10][0] - 100, face[10][1] - 50),
                        scale=2)
        elif d>100 and d<125:#if face is within 100 and 125 cm
            cvzone.putTextRect(img, 'You are a bit far',
                        (face[10][0] - 100, face[10][1] - 50),
                        scale=2)
        
        elif d>125:#if the face if far than 125 cm
            cvzone.putTextRect(img, 'You are far',
                        (face[10][0] - 100, face[10][1] - 50),
                        scale=2)

        elif d<40 and d>30:#if the face is within 40 and 30cm
            cvzone.putTextRect(img, 'You are close',
                        (face[10][0] - 100, face[10][1] - 50),
                        scale=2)
        
        else:#if the face is within 30cm
            cvzone.putTextRect(img, 'You are too close',
                        (face[10][0] - 100, face[10][1] - 50),
                        scale=2)
    if hands:#if hands are detcted
        if len(hands)==2:
            hand1=hands[0]#1st hand
            hand2=hands[1]#2nd hand
            lmList1=hand1["lmList"]#Landmarks of hand1
            lmList2=hand2["lmList"]#Landmarks of hand2
            length,info,img=detector.findDistance(lmList1[8], lmList2[8],img)#find distance between index fingers of both hands in pixels
            if length<55:#if the pixel length is less than 55 cm
                break#come out of the loop so if they make a cross symbol it will close
    cv2.imshow("Image", img)#Show the output
    k=cv2.waitKey(1)&0XFF#detect any ainput from the keyboard
    if k==27 or k==ord('q'):#if it is esc or q
        break#come out of the loop
cap.release()#close the camera functionality
cv2.destroyAllWindows()#close all windows which uses computer vision
sys.exit()#closes all python files which were used to make this functional
