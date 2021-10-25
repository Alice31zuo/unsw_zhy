#comp9517 assignment 1
#z5196480
#huiyao zuo
import cv2 as cv
import numpy as np

def contrast_stretch(image_before):     #contrast_stretch form lab 1 use to suit the varity of grey value in 0~255
    a,b = 0,255
    c,d = np.min(image_before),np.max(image_before)
    image_after = (image_before - c)*((b-a)/(d-c)) + a
    return image_after.astype(np.uint8)


def max_filtering(image_before, N):      #replace the pixel with the max pixe value around it in n* n aera

    image_after = image_before.copy()

    padding = N // 2

    img_padded = cv.copyMakeBorder(image_before, padding, padding, padding, padding, cv.BORDER_CONSTANT, value=0)

    for i in range(padding, img_padded.shape[0] - padding):
        for j in range(padding, img_padded.shape[1] - padding):
            padding_area = np.array(img_padded[i - padding:i + padding+1, j - padding:j + padding+1])
            padding_area[padding , padding ] = 0
            image_after[i - padding, j - padding] = np.max(padding_area)

    return image_after

def min_filtering(image_before,N):       #replace the pixel with the min pixe value around it in n*n aera

    image_after = image_before.copy()

    padding = N // 2

    img_padded = cv.copyMakeBorder(image_before, padding, padding, padding, padding, cv.BORDER_CONSTANT, value=255)

    for i in range(padding, img_padded.shape[0] - padding):
        for j in range(padding, img_padded.shape[1] - padding):
            padding_area = np.array(img_padded[i - padding:i + padding+1, j - padding:j + padding+1])
            padding_area[padding , padding ] = 255
            image_after[i - padding, j - padding] = np.min(padding_area)

    return image_after

def white_background(image , N):          #when the back gound is white ,need max filtering first

    image_a = max_filtering(image, N)

    image_b = min_filtering(image_a,N)

    image_after = contrast_stretch(image.astype(np.int16) - image_b.astype(np.int16))

    return image_a , image_b , image_after


def black_background(image , N):              #when the back gound is black ,need min filtering first

    image_a = min_filtering(image, N)

    image_b = max_filtering(image_a, N)

    image_after = contrast_stretch(image.astype(np.int16) - image_b.astype(np.int16))

    return image_a, image_b, image_after


def extend_M(M , N ,image):                  #when m = 0 ,mean the backgound is white ,m =1 is black
    if M == 0 :
        return white_background(image , N)
    elif M == 1 :
        return black_background(image, N)
    else:
        print('input M error')



image_1 = cv.imread('Particles.png',0)

image_2 = image = cv.imread('Cells.png',0)


#task 1 & 2

M = 0

N = 13

image_a_1, image_b_1, image_after_1 = extend_M( M , N ,image_1)

image_b_i = min_filtering(image_1,N)


#task 3
M = 1

N = 19

image_a_2, image_b_2, image_after_2 = extend_M( M , N ,image_2)

#results

cv.imshow("Image1",image_a_1)
cv.imshow("Image2",image_b_1)
cv.imshow("Image3",image_after_1)
cv.imshow("Image4",image_b_i)
cv.imshow("Image5",image_a_2)
cv.imshow("Image6",image_b_2)
cv.imshow("Image7",image_after_2)

cv.waitKey(5000000)
cv.destroyAllWindows()






