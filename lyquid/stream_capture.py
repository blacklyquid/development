# stream_capture.py

import cv2, imutils

class stream_capture:
	
	def __init__(self, stream_url):
		self.url = stream_url
		self.stream = cv2.VideoCapture(self.url)
		self.frame = None
		self.new_frame = False
		if not self.stream.isOpened():
			sys.exit('Having trouble opening video stream.' + self.url)

	def get_blob(self):
            if not self.new_frame:
                self.read()
            self.frame = imutils.resize(self.frame, width=400)
            blob = cv2.dnn.blobFromImage(cv2.resize(self.frame, (300, 300)), 0.007843, (300, 300), 127.5)
            self.new_frame = False
            return blob
	
	def read(self):
        	self.new_frame = True
		ret, self.frame = self.stream.read()

    def to_jpeg_bytes(self):
        if not self.frame:
            self.read()
        ret, jpeg = cv2.imencode('.jpg', self.frame)
        return jpeg.tobytes()
    
	def __del__(self):
		self.stream.release()
