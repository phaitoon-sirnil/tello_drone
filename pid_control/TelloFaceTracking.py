import numpy as np
from djitellopy import tello
import cv2
import time
import KeypressModule as kp

kp.init()
me = tello.Tello()
me.connect()
print(me.get_battery())

me.streamon()
#me.takeoff()
#me.send_rc_control(0, 0, 23, 0)
# time.sleep(2.2)
#time.sleep(3)

w,h = 640, 480 #360, 240
fbRage = [6200,6800]
pid = [0.4,0.4,0]
pError = 0

def findFace(img):
    faceCascade = cv2.CascadeClassifier("Resources/haarcascade_frontalface_default.xml")
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray, 1.2,8)

    myFaceListC = []
    myFaceListArea = []

    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
        cx = x + w // 2
        cy = y + h // 2
        area = w*h
        cv2.circle(img,(cx,cy),5,(0,255,0),cv2.FILLED)
        myFaceListC.append([cx,cy])
        myFaceListArea.append(area)
    if len(myFaceListArea) != 0:
        i = myFaceListArea.index(max(myFaceListArea))
        return img, [myFaceListC[i],myFaceListArea[i]]
    else:
        return img, [[0,0],0]

def trackFace(info,w,pid,pError):
    lr, ud = 0, 0
    interval = 50

    area = info[1]
    x,y = info[0]
    fb = 0

    error = x - w//2
    speed = pid[0] * error + pid[1]*(error-pError)
    speed = int(np.clip(speed,-100,100))

    if area > fbRage[0] and area < fbRage[1]:
        fb = 0
    if area > fbRage[1]:
        fb = -20
    elif area < fbRage[0] and area != 0:
        fb = 20

    if x == 0:
        speed = 0
        error = 0

    if kp.getKey("LEFT"): lr = -interval
    elif kp.getKey("RIGHT"): lr = interval

    if kp.getKey("UP"): fb = interval
    elif kp.getKey("DOWN"): fb = -interval

    if kp.getKey("w"): ud = interval
    elif kp.getKey("s"): ud = -interval

    if kp.getKey("a"): speed = interval
    elif kp.getKey("d"): speed = -interval

    if kp.getKey("q"):
        me.land()
        print("Landing...")
        time.sleep(5)
    if kp.getKey("e"): yv = me.takeoff()


    me.send_rc_control(lr,fb,ud,speed)
    # print(error,speed,fb)
    return error

# cap = cv2.VideoCapture(0)

while True:
    # _,img = cap.read()
    img = me.get_frame_read().frame
    img = cv2.resize(img,(w,h))
    img, info = findFace(img)
    pError = trackFace(info,w,pid,pError)
    # print("Center", info[0],"Area",info[1])
    cv2.imshow("Output",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        me.land()
        print("End...")
        break
