from pathlib import Path
import cv2 as cv

# Dataset paths
# inputPath = Path("D:\FinalProjectVisualOdometry\data\pmoreels-3d\Horse\Bottom")
inputPath = Path("C:/Users/cagda/Desktop/LSD_SLAM/data_odometry_gray/dataset/sequences/00/image_0")

# Lucas-Kanade Tracker parameters
lk_params = dict(winSize=(15, 15),
                 maxLevel=2,
                 criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))


# Parameters for goodFeaturesToTrack
feature_params = dict(maxCorners=500,
                      qualityLevel=0.3,
                      minDistance=7,
                      blockSize=7)

