# main.py

import time

from flask import Flask, render_template, Response

from lyquid.config import Config
from lyquid.detected_object import detected_object
from lyquid.object_detector import object_detector
from lyquid.paho_mqtt import paho_mqtt
from lyquid.stream_capture import stream_capture

app = Flask(__name__)
mqtt = paho_mqtt( Config.MQTT_CLIENT_ID, Config.MQTT_USER, Config.MQTT_PASSWORD, Config.MQTT_HOST, Config.MQTT_PORT, Config.THROTTLE_TIME)
detector = object_detector(Config.MIN_CONFIDENCE, Config.FILE_PROTOTXT, Config.FILE_MODEL)
vs = stream_capture(Config.STREAM_URL)

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(vs),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
  
if __name__ == "__main__":
	
	app.run(host='0.0.0.0', debug=True)
	
	# sleeping might reset connection on camera
	print("Waiting 60 seconds to start ...",flush=True)
	time.sleep(60.0)
	print("Begining...",flush=True)

	while True:
		detections = detector.get_detections( vs.get_blob() )
		for detection in detections:
			mqtt.publish( Config.MQTT_TOPIC + "/" + detection.label, str(detection) )
