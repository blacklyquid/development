# main.py
import numpy as np
import cv2
import time
from flask import Flask, render_template, Response

from config import Config

app = Flask(__name__)

COLORS = np.random.uniform(0, 255, size=(len(Config.CLASSES), 3))

net = cv2.dnn.readNetFromCaffe(Config.FILE_PROTOTXT, Config.FILE_MODEL)

if Config.GPU_SUPPORT:
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
    
cap = cv2.VideoCapture(Config.STREAM_URL)

@app.route('/')
def index():
	return render_template('index.html')

def gen():
	while True:
		ret, frame = cap.read()
		if not ret:
			break
		#frame = cv2.resize(frame, (300, 300))
		h, w = frame.shape[:2]
		blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5)
		net.setInput(blob)
		detections = net.forward()
		for i in np.arange(0, detections.shape[2]):
			confidence = detections[0, 0, i, 2]
			if confidence > Config.MIN_CONFIDENCE:
				idx = int(detections[0, 0, i, 1])
				box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
				(startX, startY, endX, endY) = box.astype("int")
				label = "{}: {:.2f}%".format(Config.CLASSES[idx],confidence*100)
				cv2.rectangle(frame, (startX, startY), (endX, endY),    COLORS[idx], 2)
				y = startY - 15 if startY - 15 > 15 else startY + 15
				cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
		ret, jpeg = cv2.imencode('.jpg', frame)
		yield (b'--frame\r\n'
			b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
	return Response(gen(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":

    app.run(host='0.0.0.0', debug=True)
