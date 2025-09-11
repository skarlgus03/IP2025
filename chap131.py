import cv2
import numpy as np



img = cv2.imread('citycut.jpg',1)
img_copy = img.copy()
drawing = False
sx, sy = -1,-1
font = cv2.FONT_ITALIC

def nothing(x) :
    pass

def draw_rectangle(event,x,y,flags,param):
    global sx,sy, drawing, img_copy
    
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        sx, sy = x,y
        
    elif event == cv2.EVENT_MOUSEMOVE:
        
        
        img_copy = img.copy()
        txt = 'Mouse Position ('+str(x)+','+str(y)+')' +str(img[y,x])
        cv2.putText(img_copy,txt,(10,25), font, 1,(255,255,255),2,cv2.LINE_AA)
        
        if drawing == True:
            
            cv2.rectangle(img_copy,(sx,sy),(x,y), (0,255,0),2)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        Ex , Ey = x,y
        
        x1 = min(sx,Ex)
        y1 = min(sy,Ey)
        x2 = max(sx,Ex)
        y2 = max(sy,Ey)
        
        r = cv2.getTrackbarPos('R','image')
        
        img[y1:y2,x1:x2,2] = r
        
        img_copy = img.copy()



cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_rectangle)
cv2.createTrackbar('R','image',0,255,nothing)


while(1):
    
    cv2.imshow('image',img_copy)
    k= cv2.waitKey(1)&0xFF
    if k ==27:
        break
cv2.destroyAllWindows()