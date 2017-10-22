import paho.mqtt.client as mqtt
import ssl
import json,time
import paho.mqtt.publish as publish
from datetime import datetime
import blescan
import sys

import bluetooth._bluetooth as bluez

def on_connect(mqttc, obj, flags, rc):
    if rc==0:
        print ("Subscriber Connection status code: "+str(rc)+" | Connection status: successful")
    else :
        print("Connection unsuccessful! (Result code "+str(rc) +": "+RESULT_CODES[rc] +")")
        client.disconnect()


def on_publish(client, userdata, mid):
    print(client, userdata, mid)
    #client.disconnect()


#Connect to AWS IoT
client = mqtt.Client(client_id="Rtils",protocol=mqtt.MQTTv311)
client.on_connect=on_connect
client.on_publish=on_publish
client.tls_set("/home/pi/aws/root-CA.crt",certfile="/home/pi/aws/Rtils.cert.pem",keyfile="/home/pi/aws/Rtils.private.key",tls_version=ssl.PROTOCOL_SSLv23,ciphers=None)
client.tls_insecure_set(True)
client.connect("a3qg9ikvzvrrf6.iot.ap-southeast-1.amazonaws.com", 8883, 60)
client.loop_start()

rc=0
while rc == 0 :

    sock = bluez.hci_open_dev(0)

    blescan.hci_le_set_scan_parameters(sock)
    blescan.hci_enable_le_scan(sock)
        
    returnedList = blescan.parse_events(sock, 10)

    mac=''
    uuid=''
    major=''
    miner=''
    rssi=''
    for list in returnedList:
        mac=list[0:17]
        uuid=list[18:50]
        a=51
        while True:
            if list[a:a+1]==',':
                break
            else :
                major = list[51:a+1]
            a=a+1
        if len(major)==5:
            b=57
            c=57
        else:
            b=56
            c=56
            
        while True:
            if list[b:b+1]==',':
                break
            else :
                miner = list[c:b+1]
            b=b+1

        if((len(major)==5) and (len(miner)==5)):
            d=63
        else:
            d=62
            
        rssi = list[d:len(list)]
            
        data = {}
        print('send')
        print('')
        data['uuid']=uuid
        data['mac']=mac
        data['major']=major
        data['miner']=miner
        data['rssi']=rssi
        
        payload =json.dumps(data)
        print(payload)
        msg_info=client.publish("RTILS", payload, qos=1)
        
        time.sleep(1)

