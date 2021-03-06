from pathlib import Path
import cv2 as cv
import numpy as np

# Dataset paths
# inputPath = Path("D:\FinalProjectVisualOdometry\data\pmoreels-3d\Horse\Bottom")
inputPath = Path("C:/Users/cagda/Desktop/LSD_SLAM/data_odometry_gray/dataset/sequences/09/image_0")
# inputPath = Path("D:\AGZ\MAV Images")
# inputPath = Path("C:/Users/cagda/Desktop/mav01/cam0/data")

localPathThresh = 250

# Lucas-Kanade Tracker parameters
lk_params = dict(winSize=(15, 15),
                 maxLevel=2,
                 criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))


# Parameters for goodFeaturesToTrack
feature_params = dict(maxCorners=500,
                      qualityLevel=0.3,
                      minDistance=7,
                      blockSize=7)

dist = np.array([-0.28340811, 0.07395907, 0.00019359, 1.76187114e-05])

# Values for left images(image_0) in each sequence
focalX = 718.856
focalY = 718.856
pp = (607.1928, 185.2157)

# At Şeysileri
# focalX = 4300.02832672
# focalY = 4300.02832672
# pp = (1031.89646409, 742.896640043)


# Kagaru
# focalX = 1641.99751
# focalY = 1642.30964
# pp = (642.15139, 470.34929)

# Euroc MAV dataset
# focalX = 458.654
# focalY = 457.296
# pp = (367.215, 248.375)

K = np.array([[focalX, 0, pp[0]],
              [0, focalY, pp[1]],
              [0, 0, 1]])

min_features = 1500