from djitellopy import tello
import cv2
import time

frameWidth = 640
frameHeight = 480
me = tello.Tello()
me.connect()
print(me.get_battery())

me.streamon()
while True:
    # ret , frame = cap.read()
    img = me.get_frame_read().frame
    img = cv2.resize(img,(frameWidth,frameHeight)) 

    cv2.imshow('Hello Demo Video', img)
    time.sleep(0.1)    
    if cv2.waitKey(2) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
