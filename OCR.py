import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
# import easyocr
from paddleocr import PaddleOCR,draw_ocr
import cv2



class OCR:
	def __init__(self):
		# self.reader = easyocr.Reader(['en'])
		self.reader = PaddleOCR(use_angle_cls=True, lang='en')

	def crop_name(self, img):
		H, W, _ = img.shape
		y1 = int(0.0*H)
		y2 = int(0.2*H)
		x1 = int(0.0*W)
		x2 = int(1.0*W)
		cropped = img[y1:y2,x1:x2:,:]

		return cropped

	def crop_ID(self, img):
		H, W, _ = img.shape
		y1 = int(0.6*H)
		y2 = int(0.75*H)
		x1 = int(0.6*W)
		x2 = int(1.0*W)
		cropped = img[y1:y2,x1:x2:,:]

		return cropped

	def __call__(self, img):
		name = self.crop_name(img)
		ID = self.crop_ID(img)
		cv2.imwrite("temp_name.png", name)
		cv2.imwrite("temp_ID.png", ID)
		result = self.reader.ocr("temp_name.png", cls=True)

		if len(result)>0:
			if len(result[0])>0:
				name = result[0][0][1][0]
			else:
				name = ""
		else:
			name = ""

		# print(f"Name: {name}")

		result = self.reader.ocr("temp_ID.png", cls=True)
		# print(result)
		if len(result)>0:
			if len(result[0])>0:
				ID = result[0][0][1][0]
			else:
				ID = ""
		else:
			ID = ""

		# print(f"ID: {ID}")

		return name, ID
		 
if __name__ == "__main__":

	img = cv2.imread("601193.png")
	ocr = OCR()
	ocr(img)