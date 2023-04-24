import requests
from PIL import Image
import io
import base64
import numpy
import cv2


def load_img_as_b64(path):
	with open(path, "rb") as f:
		im_bytes = f.read()

	b64_img = base64.b64encode(im_bytes).decode('UTF-8')
	return b64_img


b64_img = load_img_as_b64("test_image.png")

url = "http://127.0.0.1:5000"
data = {'image': b64_img}

resp = requests.get(url, json=data)
print(resp.json())