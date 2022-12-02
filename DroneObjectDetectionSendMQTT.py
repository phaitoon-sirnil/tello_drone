from djitellopy import tello
import cv2
import time
import matplotlib.pyplot as plt
import paho.mqtt.client as mqtt
import base64

broker = 'broker.hivemq.com'
port = 1883
username = ''
password = ''

def on_connect(client,userdata,flags,rc):
    if(rc==0):
        print("client is connected")
        global connected
        connected = True
    else:
        print("connection failed")

client = mqtt.Client()
client.username_pw_set(username,password=password)
client.on_connect = on_connect #callback function
client.on_message = on_message
client.connect(broker,port=port)
client.subscribe('/buu/mqtt/iot/image')


#import model ที่เทรนนิ่งเรียบร้อยแล้ว
config_file = 'model/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
frozen_model = 'model/frozen_inference_graph.pb'
model = cv2.dnn_DetectionModel(frozen_model,config_file)

#สร้างตัวแปรว่างๆ ไว้รับค่าจาก Labels
classLabels = []
file_labels = 'model/label.txt'

#เปิดไฟล์แล้วแต่ง String สักหน่อยให้อยู่ในรูปแบบ List 
with open(file_labels,'rt') as fpt:
    classLabels = fpt.read().rstrip('\n').split('\n')
# print('Length: ',len(classLabels))
# print(classLabels)

#กำหนดขนาดของ Input --- ศึกษาเพิ่มเติม https://docs.opencv.org/4.5.2/d3/df0/classcv_1_1dnn_1_1Model.html
model.setInputSize(320,320)
model.setInputScale(1.0/127.5)
model.setInputMean((127.5,127.5,127.5))
model.setInputSwapRB(True)
# print(model)

#เปิดภาพดูสักหน่อยครับ
# img = cv2.imread('pictures/plane-2.jpg')
# plt.imshow(img)
# plt.show()

#เปิดภาพใส่สีให้ปกติ
# plt.imshow(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
# plt.show()

# สร้างตัวแปรมารับค่า จาก model ที่เทรน เรียบร้อยแล้ว #confThreshold คือการปรับค่าสี-- ศึกษาเพิ่มเติมได้จาก https://phyblas.hinaboshi.com/oshi10
# ClassIndex, confidece , bbox  = model.detect(img,confThreshold=0.5)
# print(ClassIndex)
# print(bbox)

# สร้างกรอบรอบวัตถุ กับ ใส่ตัวหนังสือ สีแบบ BGR--- ศึกษาเพิ่มเติมได้จาก https://www.geeksforgeeks.org/python-opencv-cv2-puttext-method/
font_scale = 3
font = cv2.FONT_HERSHEY_PLAIN
colorBox = (255,0,0)
colorFont = (0,255,0)
colorPerson = (0,100,255) #bgr


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
    ClassIndex, confidece , bbox  = model.detect(img,confThreshold=0.5)
    # print(ClassIndex)
    person_count = 0
    if(len(ClassIndex) != 0):
        for ClassInd, conf, boxes in zip(ClassIndex.flatten(), confidece.flatten(), bbox):
            if(ClassInd <= 80):
                if(ClassInd==1):
                    person_count += 1
                    if(person_count>=3):
                        file_name = time.time()
                        cv2.imwrite(f'captures/{file_name}.jpg',img)
                        time.sleep(0.5)
                        with open(f'captures/{file_name}.jpg',"rb") as image:
                            img = image.read()
                        base64_bytes = base64.b64encode(img)
                        base64_message = base64_bytes.decode('ascii')
                        client.publish('/buu/mqtt/iot/image/send',base64_message)


                    cv2.rectangle(img,boxes,colorPerson)
                else:
                    cv2.rectangle(img,boxes,colorBox)
                cv2.putText(img, classLabels[ClassInd-1], (boxes[0]+10,boxes[1]+40),font,font_scale,colorFont,thickness= 3)
   
    cv2.imshow('Hello Demo Video', img)
    time.sleep(0.1)    
    if cv2.waitKey(2) & 0xFF == ord('x'):
        break

cv2.destroyAllWindows()    
