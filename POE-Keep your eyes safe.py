import cv2
import cvzone
import sys
from cvzone.FaceMeshModule import FaceMeshDetector
cap = cv2.VideoCapture(0)
detector = FaceMeshDetector(maxFaces=1)

while True:
    success, img = cap.read()
    img, faces = detector.findFaceMesh(img, draw=False)

    if faces:
        face = faces[0]
        pointLeft = face[145]
        pointRight = face[374]

        #Distance between the points
        #x=detector.findDistance(pointLeft,pointRight)
        #print(x)

        #Drawing
        #cv2.line(img, pointLeft, pointRight, (0, 200, 0), 3)
        #cv2.circle(img, pointLeft, 5, (255, 0, 255), cv2.FILLED)
        #cv2.circle(img, pointRight, 5, (255, 0, 255), cv2.FILLED)
        w, _ = detector.findDistance(pointLeft, pointRight)
        W = 6.3

        # # Finding the Focal Length
        #d = 30
        #f = (w*d)/W
        #print(f)

        # Finding distance
        f = 600
        d = (W * f) / w
        #print(d)
        cvzone.putTextRect(img,'Click esc,q or make a cross symbol to exit',(10,30),scale=1.5)
        if d>=50 and d<=100:
            cvzone.putTextRect(img, 'You are at a correct position',
                           (face[10][0] - 100, face[10][1] - 50),
                           scale=2)
        elif d>100 and d<125:
            cvzone.putTextRect(img, 'You are a bit far',
                           (face[10][0] - 100, face[10][1] - 50),
                           scale=2)
        
        elif d>125:
            cvzone.putTextRect(img, 'You are far',
                           (face[10][0] - 100, face[10][1] - 50),
                           scale=2)

        elif d<50 and d>30:
            cvzone.putTextRect(img, 'You are close',
                           (face[10][0] - 100, face[10][1] - 50),
                           scale=2)
        
        else:
            cvzone.putTextRect(img, 'You are too close',
                           (face[10][0] - 100, face[10][1] - 50),
                           scale=2)
    cv2.imshow("Image", img)
    k=cv2.waitKey(1)&0XFF
    if k==27 or k==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
sys.exit()