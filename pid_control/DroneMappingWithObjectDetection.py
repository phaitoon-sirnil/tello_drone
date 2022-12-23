import KeypressModule as kp
from djitellopy import tello
# from time import sleep
import time
import numpy as np
import cv2
import math
import matplotlib.pyplot as plt

config_file = 'Resources/model/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
frozen_model = 'Resources/model/frozen_inference_graph.pb'
model = cv2.dnn_DetectionModel(frozen_model,config_file)

classLabels = []
file_labels = 'Resources/model/labels.txt'

with open(file_labels,'rt') as fpt:
    classLabels = fpt.read().rstrip('\n').split('\n')

print(classLabels)

model.setInputSize(320,320)
model.setInputScale(1.0/127.5)
model.setInputMean((127.5,127.5,127.5))
model.setInputSwapRB(True)

img = cv2.imread('f16.jpg')
# plt.imshow(img)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.show()


##### PARAMETERS #######
fSpeed = 117/10 #Forward Speed in cm/s (15cm/s)
aSpeed = 360/10 #Angular Speed Degrees/s (50d/s)
interval = 0.25

dInterval = fSpeed*interval
aInterval = aSpeed*interval
####################################

x,y = 250,250
a = 0
yaw = 0
# global img_cam
points = [(0,0),(0,0)]

kp.init()
me = tello.Tello()
me.connect()
print(me.get_battery())

me.streamon()


def getKeyboardInput():
    lr, fb, ud, yv = 0,0,0,0

    speed = 15
    aspeed = 50
    d = 0
    global x,y,yaw,a

    if kp.getKey("LEFT"):
        lr = -speed
        d = dInterval
        a = -180
    elif kp.getKey("RIGHT"):
        lr = speed
        d = -dInterval
        a = 180

    if kp.getKey("UP"):
        fb = speed
        d = dInterval
        a = 270
    elif kp.getKey("DOWN"):
        fb = -speed
        d = -dInterval
        a = -90

    if kp.getKey("w"): ud = speed
    elif kp.getKey("s"): ud = -speed

    if kp.getKey("a"):
        yv = -aspeed
        yaw -= aInterval
    elif kp.getKey("d"):
        yv = aspeed
        yaw += aInterval

    if kp.getKey("q"): yv = me.land()
    if kp.getKey("e"): yv = me.takeoff()

    # if kp.getKey("z"):
    #     cv2.imwrite(f'Resources/Images/{time.time()}.jpg',img_cam)
    #     time.sleep(0.2)

    time.sleep(interval)
    a += yaw
    x += int(d*math.cos(math.radians(a)))
    y += int(d*math.sin(math.radians(a)))

    return [lr,fb,ud,yv,x,y]

def drawPoints(img,points):
    for point in points:
        cv2.circle(img,point,5,(0,0,255),cv2.FILLED)

    cv2.circle(img, points[-1], 8, (0, 255, 0), cv2.FILLED)
    cv2.putText(img,f'({(points[-1][0]-250)/100},{(points[-1][1]-250)/100})m',
                (points[-1][0]+10,points[-1][1]+30),cv2.FONT_HERSHEY_PLAIN,1,
                (255,0,255),1)

while True:
    vals = getKeyboardInput()
    me.send_rc_control(vals[0],vals[1],vals[2],vals[3])

    img = np.zeros((500,500,3), np.uint8)
    if(points[-1][0] != vals[4] or points[-1][1] != vals[5]):
        points.append((vals[4],vals[5]))
    drawPoints(img,points)
    cv2.imshow("Output",img)

    img_cam = me.get_frame_read().frame
    img_cam = cv2.resize(img_cam,(360,240))
    cv2.imshow("Image",img_cam)

    cv2.waitKey(1)


