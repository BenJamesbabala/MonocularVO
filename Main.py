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
from Utils import rotationMatrixToEulerAngles
import math

if __name__ == '__main__':
    vo = MonocularVO()
    trajectory = np.zeros((768, 1024, 3), np.uint8)
    annotations = None
    localErrors = np.array([])
    localRotationErrors = np.array([])
    with open(Path("C:/Users/cagda/Desktop/LSD_SLAM/data_odometry_gray/dataset/poses/09.txt")) as f:
        annotations = f.readlines()

    # Parameters.K = np.load(Path("D:\AGZ\calibration_data.npz"))["intrinsic_matrix"]
    for image in Parameters.inputPath.iterdir():
        frame = cv.imread(os.path.join(Parameters.inputPath, image), 0)
        mask = np.zeros_like(frame)
        height, width = frame.shape[:2]
        # newcameramtx, roi = cv.getOptimalNewCameraMatrix(Parameters.K, Parameters.dist, (width, height), 1, (width, height))
        # frame = cv.undistort(frame, Parameters.K, Parameters.dist, None, newcameramtx)
        # x, y, w, h = roi
        # frame = frame[y:y + h, x:x + w]
        # frame = cv.resize(frame, (width//2, height//2))
        ss = annotations[vo.tracker.frame_idx].strip().split()
        print(vo.tracker.frame_idx)
        vo.update(frame)
        if vo.tracker.frame_idx > 1:
            # vis = frame.copy()
            # cv.polylines(vis, [vo.tracker.kp1, vo.tracker.kp2], False, (0, 255, 0))
            # buildObj("dump/", vo.current_t)
            x = int(vo.current_t[0][0])+400
            y = int(vo.current_t[2][0])+90
            R = vo.current_R
            rx, ry, rz = rotationMatrixToEulerAngles(R)
            computedR = np.array([[rx], [ry], [rz]])
            trueX = int(float(ss[3]))+400
            trueY = int(float(ss[11]))+90
            trueR = np.array([[float(ss[0]), float(ss[1]), float(ss[2])],
                              [float(ss[4]), float(ss[5]), float(ss[6])],
                              [float(ss[8]), float(ss[9]), float(ss[10])]])
            trueRx, trueRy, trueRz = rotationMatrixToEulerAngles(trueR)
            trueRvector = np.array([[trueRx], [trueRy], [trueRz]])

            # buildObj("dump/groundtruth/", [[20*float(ss[1])], [20*float(ss[2])], [20*float(ss[3])]])
            cv.circle(trajectory, (x, y), 1, (0, 0, 255), 2)
            cv.circle(trajectory, (trueX, trueY), 1, (0, 255, 0))
            error = distance((x, y, 0), (trueX, trueY, 0))
            rotationError = np.linalg.norm(computedR - trueRvector)
            localErrors = np.append(localErrors, error)
            localRotationErrors = np.append(localRotationErrors, rotationError)
            draw_str(trajectory, (20, 20), "Local error %f" % (localErrors.mean()))
            draw_str(trajectory, (750, 20), "Local angular error %f" % (localRotationErrors.mean()))
            if localErrors.size >= Parameters.localPathThresh:
                localErrors = np.array([])
                localRotationErrors = np.array([])

            cv.imshow("frame", frame)

            cv.imshow("Trajectory", trajectory)
            ch = cv.waitKey(1)
            if ch == 27:
                break
    cv.imwrite("trajectory_mav_dataset.jpg", trajectory)
