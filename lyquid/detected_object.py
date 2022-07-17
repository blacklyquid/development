# detected_object.py
import time
import numpy as np
COLORS = np.random.uniform(0, 255, size=(21, 3))
class detected_object:
	labels = ["background", "aeroplane", "bicycle", "bird", 
	"boat","bottle", "bus", "car", "cat", "chair", "cow", 
	"diningtable","dog", "horse", "motorbike", "person", "pottedplant", 
	"sheep","sofa", "train", "tvmonitor"]
	def __init__(self, detected_confidence, label_index, box_info):
		self.box = box_info
		self.confidence = detected_confidence
		self.label = self.labels[label_index]
		self.timestamp = time.time()
		self.label_index = label_index
		self.color = COLORS[label_index]
		self.json_string = '{ "object":"' + self.label + '", "idx":"' + str(self.label_index) + '","confidence":"' + str(self.confidence) + '","time":"' + str(self.timestamp) + '"}'
	def __str__(self):
		return self.json_string
