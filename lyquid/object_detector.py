# object_detector.py

import cv2, time
import numpy as np
from lyquid.detected_object import detected_object

class object_detector:
	def __init__( self, min_confidence, prototxt, model ):
		self.min_confidence = min_confidence
		self.nn = cv2.dnn.readNetFromCaffe(prototxt, model)
	def get_detections( self, blob ):
		self.nn.setInput( blob )
		nn_detections = self.nn.forward()
		# detected object list to return
		dol = []
		for i in np.arange(0, nn_detections.shape[2]):
			if nn_detections[0, 0, i, 2] > self.min_confidence:
				dol.append(detected_object( nn_detections[0, 0, i, 2], int(nn_detections[0, 0, i, 1], detections[0, 0, i, 3:7])))

		return dol
