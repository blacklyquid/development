# config.py

import os, sys

class config:
	# MQTT connection
	MQTT_HOST = os.environ.get('MQTT_HOST', '192.168.1.225')     # 192.168.1.225'
	MQTT_PORT = int(os.environ.get('MQTT_PORT', 1883))           # 1883
	MQTT_CLIENT_ID = os.environ.get('MQTT_CLIENT_ID', 'obj-detection-python' )
	MQTT_USER = os.environ.get('MQTT_USER', '')
	MQTT_PASSWORD = os.environ.get('MQTT_PASSWORD','')

	# the base mqtt topic - no trailing /
	MQTT_TOPIC = os.environ.get('MQTT_TOPIC','home/object-detected')

	# The stream we are detecting objects in
	#STREAM_URL = os.environ.get('STREAM_URL','rtsp://admin:Shadow1648@192.168.1.82:554/h264Preview_01_sub')
	STREAM_URL = os.environ.get('STREAM_URL','rtsp://192.168.1.10:554/user=admin&password=&channel=1&stream=0.sdp?real_stream')
	
	# simple throttle
	# for each object detected only send MQTT message once every 30 seconds
	THROTTLE_TIME = int(os.environ.get('THROTTLE_TIME', 30))

	# Ignore detections with a confidence level lower than this, must be between 0-1
	MIN_CONFIDENCE = float(os.environ.get('MIN_CONFIDENCE', .50))
	
	FILE_PROTOTXT = "MobileNetSSD_deploy.prototxt"
	FILE_MODEL = "MobileNetSSD_deploy.caffemodel"
	
	#FILE_PROTOTXT = "SSD_MobileNet_prototxt.txt"
	#FILE_MODEL = "SSD_MobileNet.caffemodel"

	GPU_SUPPORT = int(os.environ.get('GPU_SUPPORT', 0))
		
	CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus",  "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]

Config = config();

if not Config.MQTT_HOST:
	sys.exit('Please set the MQTT_HOST enviroment variable')
if not Config.STREAM_URL:
	sys.exit('Please set the STREAM_URL enviroment variable')
if Config.MIN_CONFIDENCE > 1 or Config.MIN_CONFIDENCE < 0:
	sys.exit('Enviroment variable MIN_CONFIDENCE must be between 0 and 1')
