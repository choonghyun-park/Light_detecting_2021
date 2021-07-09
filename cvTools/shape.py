import cv2 as cv

def rescaleFrame(frame, scale=0.5):    # 프레임의 가로, 세로를 scale배 하여 반환
    # Images, Videos and live Videos 모두 적용 가능
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)

    return cv.resize(frame, dimensions, interpolation = cv.INTER_AREA)