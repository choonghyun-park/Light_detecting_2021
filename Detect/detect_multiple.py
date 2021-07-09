from imutils import contours
from skimage import measure
import numpy as np
# import argparse
import imutils
import cv2 as cv

print("\ndetect_mltiple.py launched\n")

def detect_multiple(image) : # 이미지를 받아와서 밝은 부분에 0표시를 해주는 함수
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(gray, (51, 51), 0)

    thresh = cv.threshold(blurred, 230, 255, cv.THRESH_BINARY)[1]

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

    for (i, c) in enumerate(cnts):
        # Draw the bright spot on the image
        (x,y,w,h) = cv.boundingRect(c)
        ((cX, cY), radius) = cv.minEnclosingCircle(c)
        cv.circle(image, (int(cX), int(cY)), int(radius), (0,0,255), 3)
        cv.putText(image, "#{}".format(i+1), (x,y-15),cv.FONT_HERSHEY_SIMPLEX, 0.45, (0,0,255),2)
    
    return image

