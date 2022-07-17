# main.py
import numpy as np
import cv2
import time

from flask import Flask, render_template, Response

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

def gen(camera):
	while True:
		camera.read()
		#vs.get_blob()
		detections = detector.get_detections( vs.to_blob(), camera.frame_w, camera.frame_h )
		for detection in detections:
			camera.frame_add_box(detection)
			mqtt.publish( Config.MQTT_TOPIC + "/" + detection.label, str(detection) )
		jpeg_bytes = camera.to_jpeg_bytes()
		yield (b'--frame\r\n'
			b'Content-Type: image/jpeg\r\n\r\n' + jpeg_bytes + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
	return Response(gen(vs),mimetype='multipart/x-mixed-replace; boundary=frame')
  
if __name__ == "__main__":

    app.run(host='0.0.0.0', debug=True)
		


PROTOTXT = "MobileNetSSD_deploy.prototxt"
MODEL = "MobileNetSSD_deploy.caffemodel"
INP_VIDEO_PATH = 'cars.mp4'
OUT_VIDEO_PATH = 'cars_detection.mp4'
GPU_SUPPORT = 0
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus",  "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

net = cv2.dnn.readNetFromCaffe(PROTOTXT, MODEL)
if GPU_SUPPORT:
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
    
cap = cv2.VideoCapture(INP_VIDEO_PATH)
while True:
    ret, frame = cap.read()
    if not ret:
       break
    h, w = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()
    for i in np.arange(0, detections.shape[2]):
       confidence = detections[0, 0, i, 2]
       if confidence > 0.5:
           idx = int(detections[0, 0, i, 1])
           box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
           (startX, startY, endX, endY) = box.astype("int")
           label = "{}: {:.2f}%".format(CLASSES[idx],confidence*100)
           cv2.rectangle(frame, (startX, startY), (endX, endY),    COLORS[idx], 2)
           y = startY - 15 if startY - 15 > 15 else startY + 15
           cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
 
