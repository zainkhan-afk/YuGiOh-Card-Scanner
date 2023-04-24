import cv2
import numpy as np
from utils import *

class CardDetector:
	def __init__(self):
		self.SCALE = 0.2
		self.th1 = 0
		self.th2 = 200

	def preProcess(self, image):
		R, C, _ = image.shape
		image = cv2.resize(image, (int(self.SCALE*C), int(self.SCALE*R)))

		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		gray = cv2.GaussianBlur(gray, (7,7), 0)
		# cv2.imshow("gray", gray)
		
		return gray, image
	
	def getCorners(self, gray, image, orig):
		R, C = gray.shape
		edged = cv2.Canny(gray, self.th1, self.th2)
		edged = cv2.dilate(edged, None, iterations=1)
		
		cnts, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
		cnts = sorted(cnts, key=lambda cnt:cv2.contourArea(cnt), reverse=True)

		if len(cnts) == 0:
			return None

		cnt = cnts[0]
		
		cv2.drawContours(edged, [cnt], -1, (255), thickness=-1)
		
		cnts, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
		cnts = sorted(cnts, key=lambda cnt:cv2.contourArea(cnt), reverse=True)


		cnt = cnts[0]
		
		approx = cv2.approxPolyDP(cnt, 0.1 * cv2.arcLength(cnt, True), True)
		corners = approx.reshape((approx.shape[0], approx.shape[2]))
		
		cv2.drawContours(image, [cnt], -1, (255, 0, 0), thickness=1)

		for corner in corners:
			cv2.circle(image, (corner[0], corner[1]), 5, (0,0,255))
		
		if len(corners)==4:
			warped = getPerspectiveTransform(image, corners)
			warpedOrig = getPerspectiveTransform(orig, corners/self.SCALE)
			# cv2.imshow("warped", warpedOrig)
		
		else:
			warped = image.copy()
			warpedOrig = image.copy()
		
		# cv2.imshow("E", edged)
		return warped, warpedOrig



	def __call__(self, image):
		orig = image.copy()
		gray, image = self.preProcess(image)
		warped_imgs = self.getCorners(gray, image, orig)
		# cv2.imshow("Frame", image)
		return warped_imgs



if __name__ == "__main__":
	CD = CardDetector()


	cap = cv2.VideoCapture("20230301_134850.mp4")
	# cap = cv2.VideoCapture(0)

	while True:
		ret, img = cap.read()
		# print(img.shape)
		img = CD(img)
		# cv2.imshow("img", img)
		k = cv2.waitKey(30)

		if k == ord("q"):
			break