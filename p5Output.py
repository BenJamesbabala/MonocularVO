from p5 import *
from VisualOdometry import MonocularVO
import Parameters
import numpy as np
from pathlib import Path
import cv2 as cv
import os
from Utils import buildObj
from ast import literal_eval
from FileCapture import FileCapture

capture = FileCapture()
vo = MonocularVO()
trajectory = []


def setup():
    size(800, 600)
    background(0)


def draw():
    translate(width/2, height/2)
    stroke(Color(255, 0, 0))
    fill(Color(255, 0, 0))
    frame = capture.read_frame()
    vo.update(frame)
    if vo.tracker.frame_idx > 1:
        x = int(vo.current_t[0][0])
        y = int(vo.current_t[2][0])
        circle((x, y), 4)
        trajectory.append((x, y))
    print(len(trajectory), vo.tracker.frame_idx)
    if vo.tracker.frame_idx > 2:
        stroke(Color(255, 255, 255))
        fill(Color(255, 255, 255))
        circle(trajectory[-2], 4)


if __name__ == '__main__':
    run(frame_rate=30)