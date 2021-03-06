import os
import sys

sys.path.append(".")
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))) # Light_detecting_2021

import Detect.detect_multiple as detect
import cvTools
import cv2 as cv

# module import
def main() :
    # Reading videos
    capture = cv.VideoCapture(0)

    # Read from path
    # path = "C:/Users/user/Desktop/University/012. HEVEN/009. 기술아이디어/Videos"
    # capture = cv.VideoCapture(path+"/tunnel2.mp4")


    while True:
        isTrue, frame = capture.read()
        
        try:
            detect_frame = detect.detect_multiple(frame)

            # rescale_frame = cvTools.shape.rescaleFrame(detect_frame)
            

            cv.imshow('Video', detect_frame)

            # cv.imshow('Video', rescale_frame)

            if cv.waitKey(1) & 0xFF==ord('d'):
                break
        except:
            cv.imshow('Video', frame)
            if cv.waitKey(1) & 0xFF==ord('d'):
                break
    capture.release()
    cv.destroyAllWindows()

    return 0

if __name__ == "__main__":
    if main() == 0:
        print("\nLight_Detecting terminated successfully!")
    else:
        print("\nThere is something wrong. I recommend you to kill every processes which is related to this program.")
    