# MQTT
# import ibmiotf.application
import paho.mqtt.client as mqtt
import time
import json
import Adafruit_DHT

# External module imports                                                                                                        
import RPi.GPIO as GPIO

sensor = Adafruit_DHT.DHT11

gpio1 = 17
gpio2 = 22

message = {}


def getTempHum():
	while(True):
            
            humi, tempi = Adafruit_DHT.read_retry(sensor, gpio1)
            humo, tempo = Adafruit_DHT.read_retry(sensor, gpio2)
                
            if humi is not None and tempi is not None and humo is not None and tempo is not None:
                print('Tempin={0:0.1f}*C  Humin={1:0.1f}%'.format(tempi, humi))
                print('Tempout={0:0.1f}*C  Humout={1:0.1f}%'.format(tempo, humo))
            else:
                print('Failed to get reading. Try again!')

            message.update({"sensor_in":{"temp":tempi,"hum":humi},"sensor_out":{"temp":tempo,"hum":humo}})	
            print (message)
            mqtt_Send(json.dumps(message),"temp-hum-ps")

            time.sleep(5)


# def on_message(client, userdata, msg):
#     print(msg.topic+" "+str(msg.payload))	


def on_connect(client, userdata, flags, rc):
	print ("MQTT Connected with result code"+str(rc))
	

def mqtt_Send(message,channel):
	(result,mid) = mqttc.publish(channel,message,1)
	print (mid)
	print (result)

def mqtt_Init(mqtt_hostName,mqtt_portnumber,timealive):
	global mqttc
	mqttc = mqtt.Client()
	mqttc.on_connect = on_connect
	# mqttc.on_message = on_message

	mqttc.connect(mqtt_hostName,mqtt_portnumber,timealive)


if __name__ == '__main__':
	mqtt_hostName = '34.226.134.195' # give the ip address of the system where you have installed the broker
	mqtt_portnumber = 1883 # mqtt default port number
	timealive = 60 # mqtt connection check interval time
	mqtt_Init(mqtt_hostName,mqtt_portnumber,timealive)
	getTempHum()