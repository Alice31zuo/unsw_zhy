#lab 1 z5196480
import matplotlib.pyplot as plt
import cv2 as cv
import numpy as np

image = cv.imread("cat.png",0)

def contrast_stretch(image_before):
    a,b = 0,255
    c,d = np.min(image_before),np.max(image_before)
    image_after = (image_before - c)*((b-a)/(d-c)) + a
    return image_after.astype(np.uint8)

blur = cv.GaussianBlur(image,(21,21),0)

h_image = image.astype(np.int16) - blur.astype(np.int16)

image_final = image.astype(np.int16) + h_image*1.4

h_image_after = contrast_stretch(image_final)

#orignal_image_strach = contrast_stretch(image)
cv.imshow("Image1",image)

cv.imshow("Image3",h_image_after)

cv.imwrite("cat_edge.png", h_image_after)

cv.waitKey(10000)
cv.destroyAllWindows()