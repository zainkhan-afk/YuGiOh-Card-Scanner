import cv2
import numpy as np
from scipy.spatial import distance as dist

SCALE = 0.5

def getDist(pt1, pt2):
	return np.sqrt((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2)

def orderPts(pts):
	sortedByX = pts[np.argsort(pts[:, 0]), :]
	
	left = sortedByX[:2, :]
	right = sortedByX[2:, :]
 
	left = left[np.argsort(left[:, 1]), :]
	(tl, bl) = left
	
	D = dist.cdist(tl[np.newaxis], right, "euclidean")[0]
	(br, tr) = right[np.argsort(D)[::-1], :]

	orderedPts = np.array([tl, tr, br, bl]).astype("float32")
 
	return orderedPts

def getPerspectiveTransform(image, pts):
	
	pts = orderPts(pts)
	(tl, tr, br, bl) = pts

	widthA = getDist(br, bl)
	widthB = getDist(tr, tl)
	
	maxWidth = max(int(widthA), int(widthB))

	heightA = getDist(tr, br)
	heightB = getDist(tl, bl)
	
	maxHeight = max(int(heightA), int(heightB))

	dst = np.array([
		[0, 0],
		[maxWidth - 1, 0],
		[maxWidth - 1, maxHeight - 1],
		[0, maxHeight - 1]]).astype("float32")

	M = cv2.getPerspectiveTransform(pts, dst)
	warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

	return warped