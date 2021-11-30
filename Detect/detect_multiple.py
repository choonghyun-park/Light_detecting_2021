from imutils import contours
from skimage import measure
import numpy as np
# import argparse
import imutils
import cv2 as cv
import serial
import time

ser = serial.Serial('/dev/ttyUSB0',9600)
print("\ndetect_mltiple.py launched\n")
ser.write(b'a')
print("\n============time sleep 1===========\n")
time.sleep(1)

def detect_multiple(image) : 
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(gray, (51, 51), 0)
    thresh = cv.threshold(blurred, 240, 255, cv.THRESH_BINARY)[1]

    thresh = cv.erode(thresh, None, iterations=2)
    thresh = cv.dilate(thresh, None, iterations=4)

    labels = measure.label(thresh, connectivity=2, background=0)
    mask = np.zeros(thresh.shape, dtype = "uint8")

    # loop over the unique components
    for label in np.unique(labels):
        if label == 0 :
            continue
            
        labelMask = np.zeros(thresh.shape, dtype="uint8")
        labelMask[labels == label] = 255
        numPixels = cv.countNonZero(labelMask)
        if numPixels > 300:
            mask = cv.add(mask, labelMask)

    cnts = cv.findContours(mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = contours.sort_contours(cnts)[0]
    
    lst = []
    time.sleep(0.1)
    print("\n============time sleep 0.1===========\n")
    # ser.write(b'a')
    for (i, c) in enumerate(cnts):
        # Draw the bright spot on the image
        (x,y,w,h) = cv.boundingRect(c)
        spot = destination(x,y,w,h)
        
        if (spot is not None):
            if spot not in lst:
                lst.append(spot)
            print("Detected Square : ", spot)
            ser.write(int2bin(spot))
            
        ((cX, cY), radius) = cv.minEnclosingCircle(c)
        cv.circle(image, (int(cX), int(cY)), int(radius), (0,0,255), 3)
        cv.putText(image, "#{}".format(i+1), (x,y-15),cv.FONT_HERSHEY_SIMPLEX, 0.45, (0,0,255),2)
    offSpot(lst)

    return image

def destination(x,y,w,h):
    dest_x=x+w/2
    dest_y=y+h/2
    if dest_x<160 and dest_y>240:
        return 1
    elif dest_x<160 and dest_y<=240:
        return 2
    elif 160<=dest_x<320 and dest_y<=240:
        return 3
    elif 320<=dest_x<480 and dest_y<=240:
        return 4
    elif 480<=dest_x<640 and dest_y>240:
        return 5
    elif 480<=dest_x<640 and dest_y>240:
        return 6
    else:
        pass

def int2bin(i):
    if i == 1:
        return b'1'
    elif i == 2:
        return b'2'
    elif i == 3:
        return b'3'
    elif i == 4:
        return b'4'
    elif i == 5:
        return b'5'
    elif i == 6:
        return b'6'
    else :
        return 

def offSpot(lst):
    if 1 not in lst:
        ser.write(b'A')
    if 2 not in lst:
        ser.write(b'B')
    if 3 not in lst:
        ser.write(b'C')
    if 4 not in lst:
        ser.write(b'D')
    if 5 not in lst:
        ser.write(b'E')
    if 6 not in lst:
        ser.write(b'F')

# def lst2bin(lst):
#     ret = 0b000000
#     if 1 in lst:
#         ret += 0b010000
#     if 2 in lst:
#         ret += 0b010000
#     if 3 in lst:
#         ret += 0b001000
#     if 4 in lst:
#         ret += 0b000100
#     if 5 in lst:
#         ret += 0b000010
#     if 6 in lst:
#         ret += 0b000001
    
#     return ret

# def write_read(x):
#     ser.write(bytes(x, 'utf-8'))
#     time.sleep(0.05)
#     data = ser.readline()
#     return data
