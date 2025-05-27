from pynput import keyboard
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
client.username_pw_set("snake", 'tre]:7T"gm:TZ5a')
client.connect(host, 8883)

def on_publish(client, userdata, mid):
    print("mid: "+str(mid))

keys = (keyboard.KeyCode.from_char('w'),
        keyboard.KeyCode.from_char('a'),
        keyboard.KeyCode.from_char('s'),
        keyboard.KeyCode.from_char('d'))
direction = ('UP','LEFT','DOWN','RIGHT')

pressed_keys = set()

def on_press(key):
    # only send once per actual press
    if key in keys and key not in pressed_keys:
        pressed_keys.add(key)
        client.publish("snake/input_direction",
                       direction[keys.index(key)])
    elif key == keyboard.Key.esc:
        return False

def on_release(key):
    # clear key so next press will fire again
    if key in pressed_keys:
        pressed_keys.remove(key)
    # stop listener on Esc
    if key == keyboard.Key.esc:
        return False

with keyboard.Listener(
        on_press=on_press,
        on_release=on_release
) as listener:
    listener.join()