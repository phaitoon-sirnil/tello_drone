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

client = mqtt.Client()
client.username_pw_set(username,password=password)
client.on_connect = on_connect #callback function
client.on_message = on_message
client.connect(broker,port=port)
client.subscribe('/buu/mqtt/iot/image/received')


client.publish('/buu/mqtt/iot/image/send','Hello mqtt') #send to MQTT-Dash App
print('Send Hello.....')

client.loop_forever()
