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

def on_message(client,userdata,message):
    print('message is coming...')

client = mqtt.Client()
client.username_pw_set(username,password=password)
client.on_connect = on_connect #callback function
client.on_message = on_message
client.connect(broker,port=port)
client.subscribe('/buu/mqtt/iot/image')

with open("static/images/address02.jpg","rb") as image:
    img = image.read()

message = img
# open('hotrrr.jpg','wb').write(message)

base64_bytes = base64.b64encode(message)
base64_message = base64_bytes.decode('ascii')
# print(base64_message)
# client.publish('/buu/mqtt/iot/image/send',base64_message)
client.publish('/buu/mqtt/app/image/send',img) #send to MQTT-Dash App
client.publish('/buu/mqtt/image/send',base64_message)
client.loop_forever()
