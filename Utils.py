import cv2 as cv
import numpy as np


# OpenCV function -> samples/python/common.py
def draw_str(dst, target, s):
    x, y = target
    cv.putText(dst, s, (x + 1, y + 1), cv.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 0), thickness=2, lineType=cv.LINE_AA)
    cv.putText(dst, s, (x, y), cv.FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255), lineType=cv.LINE_AA)


# Generates projection matrix P using the given K, R, t
def projection_from_KRt(K, R, t):
    return cv.hconcat(np.dot(K, R), np.dot(K, t))
