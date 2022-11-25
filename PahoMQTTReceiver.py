
import paho.mqtt.client as mqtt

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
    msg = str(message.payload.decode('utf-8'))
    print(msg)

client = mqtt.Client()
client.username_pw_set(username,password=password)
client.on_connect = on_connect #callback function
client.on_message = on_message #callback function
client.connect(broker,port=port)

# client = mqtt.Client()
# client.connect('broker.hivemq.com')
client.subscribe('/buu/mqtt/iot/image/send')

# client.on_message = on_message
# client.on_connect = on_connect
client.loop_forever()
