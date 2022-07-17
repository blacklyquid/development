# stream_capture.py

import cv2, imutils
import numpy as np

class stream_capture:

	def __init__(self, stream_url):
		self.url = stream_url
		self.stream = cv2.VideoCapture(self.url)
		self.frame = None
		self.new_frame = False
		if not self.stream.isOpened():
			sys.exit('Having trouble opening video stream.' + self.url)

	def to_blob(self):
		if not self.new_frame:
			self.read()
		self.frame = imutils.resize(self.frame, width=400)
		self.frame_h, self.frame_w = frame.shape[:2]
		blob = cv2.dnn.blobFromImage(cv2.resize(self.frame, (300, 300)), 0.007843, (300, 300), 127.5)
		self.new_frame = False
		return blob

	def read(self):
		self.new_frame = True
		ret, self.frame = self.stream.read()

	def to_jpeg_bytes(self):
		ret, jpeg = cv2.imencode('.jpg', self.frame)
		return jpeg.tobytes()
	def frame_add_box(self, object):
		box = object.box * np.array([self.frame_w, self.frame_h, self.frame_w, self.frame_h])
           	(startX, startY, endX, endY) = box.astype("int")
           	label = "{}: {:.2f}%".format(object.label,confidence*100)
           	cv2.rectangle(self.frame, (startX, startY), (endX, endY), object.color, 2)
           	y = startY - 15 if startY - 15 > 15 else startY + 15
           	cv2.putText(self.frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
	def __del__(self):
		self.stream.release()
