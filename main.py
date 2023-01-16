# from pyModbusTCP.client import ModbusClient
import paho.mqtt.client as mqtt
import re, uuid
# import time
# import requests

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True #set flag
        print("MQTT Broker Connected")
    else:
        client.connected_flag=False
        print("Bad connection Returned code =",rc)
    client.subscribe("devices/SNF412FA4029AC/data")

def bridge(data):
    # print(data)
    if((data.find("Addr=101"))!=-1):
        topicpub= "devices/" + "SNF412FA4029AC_1" + "/data"
        data=data.replace("SNF412FA4029AC", "SNF412FA4029AC_1")
    if(((data.find("Addr=102"))!=-1) or ((data.find("Addr=103"))!=-1)):
        topicpub= "devices/" + "SNF412FA4029AC_2" + "/data"
        data=data.replace("SNF412FA4029AC", "SNF412FA4029AC_2")
    if(((data.find("Addr=104"))!=-1) or ((data.find("Addr=105"))!=-1)):
        topicpub= "devices/" + "SNF412FA4029AC_3" + "/data"  
        data=data.replace("SNF412FA4029AC", "SNF412FA4029AC_3")  
    client.publish(
                topic = topicpub,
                payload = data,
                qos = 2)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    result=(msg.payload).decode("utf-8")
    bridge(result)

   
def mqttpublish(topic, data):
    publish_result=client.publish(topic, data, qos=0, retain=False)
    publish_result.wait_for_publish()
    timeout=0
    while (publish_result.is_published()==False):
      time.sleep(1)
      if(timeout==5):
        print("MQTT Pub timeout!")
        break
      timeout+=1
    if(timeout<5):
      print("MQTT Published!")
      return True
    else:
      print("MQTT not Publish!")
      return False

try:
  MAC = re.findall('..', '%012x' % uuid.getnode())
  measurement= "SN" + str(MAC[0]).upper() + str(MAC[1]).upper() + str(MAC[2]).upper() + str(MAC[3]).upper() + str(MAC[4]).upper() + str(MAC[5]).upper()
  ########################## MQTT Broker Setup #########################
  client = mqtt.Client(client_id="device-" + measurement, clean_session=True, userdata=None, transport="tcp")
  client.on_connect = on_connect
  client.on_message = on_message
  MQTTusername="python"
  MQTTpassword="P@ssword2022"
  MQTThost="34.125.222.202"
  MQTTport=1883
  MQTTkeepalive=60
  client.username_pw_set(MQTTusername, password=MQTTpassword)
  print("MQTT Connecting!")
  client.connect(MQTThost, MQTTport, MQTTkeepalive)
  client.loop_forever()
  ######################### MQTT Broker Setup #########################
except ValueError:
  print("Error with host or port params")
