import numpy as np
import cv2

img = np.zeros((640,451,3), np.uint8)

img = cv2.imread('Random.jpg',1)

img = cv2.line(img,(0,0),(640,451),(255,0,0),3)

img = cv2.rectangle(img,(400,0),(640,240),(0,255,0),3)

img = cv2.circle(img,(520,120), 120, (0,0,255), 4)

img = cv2.ellipse(img,(200,300),(100,50),0,0,360,255,3)

font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(img,'OpenCV',(10,400), font, 3,(255,255,255),12,cv2.LINE_AA)



cv2.imshow('frame',img)
k = cv2.waitKey(0)
if k == 27:
    cv2.destroyAllWindows()
