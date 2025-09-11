import cv2
import numpy as np
from matplotlib import pyplot as plt

def nothing(x) :
    pass

img1 = cv2.imread('gosum.jpg')
img2 = cv2.imread('opencv_logo.png')

img2 = cv2.resize(img2,(278,367))


cv2.namedWindow('image')
cv2.createTrackbar('Weight','image',0,100,nothing)

while(1):
    w = cv2.getTrackbarPos('Weight','image')/100
    dst = cv2.addWeighted(img1,w,img2,1-w,0)   
    cv2.imshow('image',dst)
    k= cv2.waitKey(1)&0xFF
    if k ==27:
        break
cv2.destroyAllWindows()