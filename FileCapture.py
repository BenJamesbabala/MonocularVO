from Parameters import inputPath
import os
import cv2 as cv

class FileCapture:
    def __init__(self):
        self.frame_no = 0
        self.frames = list(inputPath.iterdir())

    def read_frame(self):
        self.frame_no += 1
        return cv.imread(os.path.join(inputPath, self.frames[self.frame_no-1]), 1)