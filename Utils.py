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


def find_matches(src_des, src_kp, train_des, train_kp, numOfGoodMatches=50, matcher=cv.BFMatcher()):
    matches = matcher.knnMatch(src_des, train_des, k=2)

    good = []

    for m, n in matches:
        if m.distance < 0.60 * n.distance:
            good.append(m)
    src_points = []
    dst_points = []

    for m in good:
        matches[src_kp[m.queryIdx].pt] = train_kp[m.trainIdx].pt
        src_points.append(src_kp[m.queryIdx].pt)
        dst_points.append(train_kp[m.trainIdx].pt)

    return np.array(src_points), np.array(dst_points)
