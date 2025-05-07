import keyboard
import paho.mqtt.client as paho
from paho import mqtt

host = "5cb42c9748844ca2bd6d0e57f6406124.s1.eu.hivemq.cloud"

def on_log(client, userdata, level, buf):
    print("log: "+buf)

def on_connect(client, userdata, flags, rc):
    print('CONNACK received with code %d.' % (rc))

client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect


client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# set username and password
client.username_pw_set("snake", 'tre]:7T"gm:TZ5a')
client.connect(host, 8883)

def on_publish(client, userdata, mid):
    print("mid: "+str(mid))

keys = ('w','a','s','d')
direction = ('UP','LEFT','DOWN','RIGHT')

prev_key = ''
while True:
    for key in keys:
        if keyboard.is_pressed(key):
            if prev_key != key:
                print(key)
                (rc,mid) = client.publish("snake/input_direction", direction[keys.index(key)])
                prev_key = key
    if keyboard.is_pressed('q'):
        print('Quitting')
        break