'''
 Based on the following tutorial:
   http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_feature2d/py_matcher/py_matcher.html
'''
import numpy as np
import cv2

class Measure():
	def __init__(self):
		self.bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
		self.k = 2
	
	def compare(self, descriptors1, descriptors2):
		matches = self.bf.knnMatch(descriptors1, descriptors2, self.k)
		goodMatches = []

		for m, n in matches:
			if m.distance < 0.75 * n.distance:
				goodMatches.append([m])
		percentage =len(goodMatches) / (max(len(descriptors1),len(descriptors2)))
		return percentage

class Descriptor():
	def __init__(self):
		self.orb = cv2.ORB_create()

	def get_descriptor(self, image):
		if len(image.shape) >= 3:
			image = cv2.cvtColor(image, 0)
		kpts, dpts = self.orb.detectAndCompute(image, None)
		return dpts

def main():
	img1 = cv2.imread('/home/tu/AI/code/aladin/BookImages/2.jpg')
	img2 = cv2.imread('/home/tu/AI/code/aladin/BookImages/7.jpg')
	measure = Measure()
	orb = Descriptor()
	dpt1 = orb.get_descriptor(img1)
	dpt2 = orb.get_descriptor(img2)
	score = measure.compare(dpt1,dpt2)
	print(type(dpt1[0][0]))
	print(score)

if __name__ == '__main__':
  	main()