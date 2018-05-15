from VisualOdometry import MonocularVO
import Parameters
import numpy as np
from pathlib import Path
import cv2 as cv
import os
from Utils import buildObj
from ast import literal_eval
from Utils import draw_str
from Utils import distance
import math

if __name__ == '__main__':
    vo = MonocularVO()
    trajectory = np.zeros((768, 1024, 3), np.uint8)
    annotations = None
    with open(Path("C:/Users/cagda/Desktop/mav01/state_groundtruth_estimate0/data.csv")) as f:
        annotations = f.readlines()

    # Parameters.K = np.load(Path("D:\AGZ\calibration_data.npz"))["intrinsic_matrix"]
    for image in Parameters.inputPath.iterdir():
        frame = cv.imread(os.path.join(Parameters.inputPath, image), 0)
        mask = np.zeros_like(frame)
        height, width = frame.shape[:2]
        # frame = cv.resize(frame, (width//2, height//2))
        ss = annotations[vo.tracker.frame_idx+1].strip().split(",")
        print(vo.tracker.frame_idx)
        vo.update(frame)
        if vo.tracker.frame_idx > 1:
            # vis = frame.copy()
            # cv.polylines(vis, [vo.tracker.kp1, vo.tracker.kp2], False, (0, 255, 0))
            buildObj("dump/", vo.current_t)
            x = int(vo.current_t[0][0])+400
            y = int(vo.current_t[2][0])+90
            trueX = int(20 * float(ss[1]))+400
            trueY = int(20 * float(ss[3]))+90
            buildObj("dump/groundtruth/", [[20*float(ss[1])], [20*float(ss[2])], [20*float(ss[3])]])
            cv.circle(trajectory, (x, y), 1, (0, 0, 255), 2)
            cv.circle(trajectory, (trueX, trueY), 1, (0, 255, 0))

            cv.imshow("frame", frame)
            draw_str(trajectory, (20, 20), "Drift in x: %f, y: %f" % (abs(trueX-x), abs(trueY-y)))

            cv.imshow("Trajectory", trajectory)
            ch = cv.waitKey(1)
            if ch == 27:
                break
    cv.imwrite("trajectory_mav_dataset.jpg", trajectory)
