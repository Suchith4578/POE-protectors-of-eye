#import eyesafer as es
from turtle import color
import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.HandTrackingModule import HandDetector
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.clock import Clock
import sys

class mainApp(MDApp):
    def build(self):
        layout=MDBoxLayout(orientation='horizontal')
        self.image=Image()
        layout.add_widget(self.image)
        self.exit=Button(
            text='Exit',
            pos_hint={'center_x':.5,'center_y': .5},
            size_hint=(None,None))
        self.exit.bind(on_press=self.pressed)
        layout.add_widget(self.exit)
        self.capture=cv2.VideoCapture(0)
        self.detector = FaceMeshDetector(maxFaces=1)#Detecting landmarks on face

        self.detector2=HandDetector(detectionCon=0.8,maxHands=2)#Detecting Landmarks on hand
        Clock.schedule_interval(self.load_video,1.0/30.0)
        return layout
    def pressed(self,instance):
        sys.exit()
    
    def load_video(self,*args):
        ret,frame=self.capture.read()
        frame, faces = self.detector.findFaceMesh(frame, draw=False)
        hands,frame=self.detector2.findHands(frame,draw=True)
        if faces:#if faces are dtected
            face = faces[0]#1st face
            pointLeft = face[145]#eyeball's landmarks
            pointRight = face[374]#eyeball's landmarks
            w, _ = self.detector.findDistance(pointLeft, pointRight)#finds the distance between the eyeballs
            W = 6.3#average width of the face of an human

            # Finding distance
            f = 600#focal length
            d = (W * f) / w #distance
            cvzone.putTextRect(frame,'Make a cross symbol or click exit button to exit ',(10,30),scale=1.5)#puts a rectangle and text on the top right of the window
            if d>=40 and d<=100:#if face is within 40 and 100cm
                cvzone.putTextRect(frame, 'You are at a correct position',
                            (face[10][0] - 100, face[10][1] - 50),
                            scale=2)
            elif d>100 and d<125:#if face is within 100 and 125 cm
                cvzone.putTextRect(frame, 'You are a bit far',
                            (face[10][0] - 100, face[10][1] - 50),
                            scale=2)
            
            elif d>125:#if the face if far than 125 cm
                cvzone.putTextRect(frame, 'You are far',
                            (face[10][0] - 100, face[10][1] - 50),
                            scale=2)

            elif d<40 and d>30:#if the face is within 40 and 30cm
                cvzone.putTextRect(frame, 'You are close',
                            (face[10][0] - 100, face[10][1] - 50),
                            scale=2)
            
            else:#if the face is within 30cm
                cvzone.putTextRect(frame, 'You are too close',
                            (face[10][0] - 100, face[10][1] - 50),
                            scale=2)
        if hands:#if hands are detcted
            if len(hands)==2:
                hand1=hands[0]#1st hand
                hand2=hands[1]#2nd hand
                lmList1=hand1["lmList"]#Landmarks of hand1
                lmList2=hand2["lmList"]#Landmarks of hand2
                length,info,img=self.detector.findDistance(lmList1[8], lmList2[8],frame)#find distance between index fingers of both hands in pixels
                if length<55:#if the pixel length is less than 55 cm
                    sys.exit()
        self.image_frame=frame
        buffer=cv2.flip(frame,0).tostring()
        texture=Texture.create(size=(frame.shape[1],frame.shape[0]),colorfmt='bgr')
        texture.blit_buffer(buffer,colorfmt='bgr',bufferfmt='ubyte')
        self.image.texture=texture

if __name__ == '__main__':
    mainApp().run()