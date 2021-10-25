#lab 1 z5196480
import matplotlib.pyplot as plt
import cv2 as cv
import numpy as np

image = cv.imread("cat.png",0)
#image_rgb = image[:,:,::-1]
#plt.imshow(image,'gray')

#question 1

def contrast_stretch(image_before):
    a,b = 0,255
    c,d = np.min(image_before),np.max(image_before)
    image_after = (image_before - c)*((b-a)/(d-c)) + a
    return image_after.astype(np.uint8)

image_after = contrast_stretch(image)


cv.imshow("Image1", image)
#cv.imshow("Image2",image_after)

cv.waitKey(5000)
cv.destroyAllWindows()
'''
#question 2

def grey_intensity(image):
    list_grey = [0 for _ in range(256)]
    for num in range(256):
        count_array = image[image == num]
        list_grey[num] = count_array.size
    return list_grey

image_list = grey_intensity(image)
print(image_list)

#np.histogram(image_list,bins=256,range=None,weights=None,density=False)


#image = np.histogram(image_list, 256, [0, 256])#hist1 每个灰度值的频数
#cdf = hist1.cumsum()#累加频数得累计直方图
#cdf_normalised = cdf * float(hist1.max() / cdf.max())#把累计直方图的比例化到近似直方图
#plt.plot(image,color='blue')
#plt.show()

bin = [i for i in range(256)]
#plt.hist(image_list, bins =256)
#plt.title("histogram")
#plt.show()
#plt.bar(x = bin,height=image_list)
#plt.show()

#question 3


Deri_x = np.array([[-1, 0, 1],[-2, 0, 2],[-1, 0, 1]])
Deri_y = np.array([[-1, -2, -1],[0, 0, 0],[1, 2, 1]])

x_egde = cv.filter2D(image, -1, Deri_x)
y_egde = cv.filter2D(image, -1, Deri_y)

all_egde = x_egde + y_egde

plt.imshow(x_egde, cmap='gray', vmin=0, vmax=255)

plt.imshow(y_egde, cmap='gray', vmin=0, vmax=255)

plt.imshow(all_egde, cmap='gray', vmin=0, vmax=255)



'''
#question 4

blur = cv.GaussianBlur(image,(21,21),0)

#plt.imshow(blur, 'gray')
#plt.show()

#cv.imshow("Image3", blur)


#cv.waitKey(5000)
#cv.destroyAllWindows()

h_image = image.astype(np.int16) - blur.astype(np.int16)
#h_image_after= contrast_stretch(h_image)
#cv.imshow("Image4", h_image_after)
#cv.imshow("Image2",image_after)

image_final = image.astype(np.int16) + h_image*1.25
h_image_after = contrast_stretch(image_final)
cv.imshow("Image5",h_image_after)

cv.waitKey(5000)
cv.destroyAllWindows()



