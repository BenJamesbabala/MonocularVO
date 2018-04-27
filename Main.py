from VisualOdometry import MonocularVO
import Parameters
import numpy as np
from pathlib import Path
import cv2 as cv
import os
from Utils import buildObj
from ast import literal_eval

if __name__ == '__main__':
    vo = MonocularVO()
    trajectory = np.zeros((600, 800, 3), np.uint8)
    # Parameters.K = np.load(Path("D:\AGZ\calibration_data.npz"))["intrinsic_matrix"]
    for image in Parameters.inputPath.iterdir():
        frame = cv.imread(os.path.join(Parameters.inputPath, image), 0)
        height, width = frame.shape[:2]
        print(vo.tracker.frame_idx)
        vo.update(frame)
        if vo.tracker.frame_idx > 1:
            # vis = frame.copy()
            # cv.polylines(vis, [vo.tracker.kp1, vo.tracker.kp2], False, (0, 255, 0))
            cv.imshow("frame", frame)
            buildObj("dump/kesinsonbukesin/", vo.current_t)
            x = int(vo.current_t[0][0])+290
            y = int(vo.current_t[2][0])+90
            cv.circle(trajectory, (x, y), 1, (0, 0, 255))
            cv.imshow("Trajectory", trajectory)
            ch = cv.waitKey(1)
            if ch == 27:
                break
    cv.imwrite("trajectory_mav_dataset.jpg", trajectory)
