import cv2,time
import matplotlib.pyplot as plt
import numpy as np
from math import ceil

def SlideShow(image_array):
	for i in image_array:
		try:
			i=cv2.resize(i,(600,600))
			cv2.imshow('Photo Frame',i)
			if (cv2.waitKey(1)&0xff) == 'q':
				break
			time.sleep(0.3)
		except KeyboardInterrupt:
			break
		except:
			pass

pic_name = 'image.jpg'
image = cv2.imread(pic_name)
image = cv2.resize(image,(600,600))
image_array=[]
image_array.append(image)
range_contrast = list(np.linspace(1,10,5))
for i in range_contrast+range_contrast[::-1]:
	contrast_img = cv2.addWeighted(image, i, np.zeros(image.shape, image.dtype), 0, 0)
	image_array.append(contrast_img)
image_array.append(image)
for i in list(range(1,11,4))+list(range(10,1,-4)):
	blur_image = cv2.GaussianBlur(image,(7,7),i)
	image_array.append(blur_image)
image_array.append(image)
edge_img = cv2.Canny(image,100,200)
image_array.append(edge_img)
image_array.append(image)
for j in ['cv2.'+i for i in dir(cv2) if i.startswith('COLOR_BGR2')]:
	try:
		cvt = cv2.cvtColor(image,eval(j))
		image_array.append(cvt)
	except:
		pass
def conturs_img(l):
	conturs = image
	gray_img = cv2.cvtColor(conturs, cv2.COLOR_BGR2GRAY)
	retval, thresh = cv2.threshold(gray_img, 127, 255, 0)
	img_contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cv2.drawContours(conturs, img_contours, -1, (0, 255, 0))
	return conturs
for i in [(255,0,0),(0,255,0),(0,0,255)]:
	image_array.append(conturs_img(i))
gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
img_contours = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2]
img_contours = sorted(img_contours, key=cv2.contourArea)
for i in img_contours:
	if cv2.contourArea(i) > 100:
		break
mask = np.zeros(image.shape[:2], np.uint8)
cv2.drawContours(mask, [i],-1, 255, -1)
new_img = cv2.bitwise_and(image, image, mask=mask)
image_array.append(new_img)
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
gray = cv2.medianBlur(gray,5)
edges = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,9,9)
color = cv2.bilateralFilter(image,9,250,250)
cartoon = cv2.bitwise_and(color,color,mask=edges)
image_array.append(edges)
image_array.append(cartoon)
SlideShow(image_array)
cv2.destroyAllWindows()
