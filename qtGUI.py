import sys
from os import path
import time
import cv2
import numpy as np
from FileCapture import*


from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui


from VisualOdometry import MonocularVO
import Parameters
import numpy as np
from pathlib import Path
import os
from Utils import buildObj
from ast import literal_eval

class TrajectoryWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.vo = MonocularVO()
        self.image = QtGui.QImage()
        self._red = (0, 0, 255)
        self._width = 2
        self._min_size = (800, 600)
        self.capture=FileCapture()
        self.vo_loop()

    def get_qimage(self, image: np.ndarray):
        height, width, colors = image.shape
        bytesPerLine = 3 * width
        QImage = QtGui.QImage

        image = QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888)

        image = image.rgbSwapped()
        return image

    def vo_loop(self):
        while self.capture.frame_no < len(self.capture.frames):
            frame = self.capture.read_frame()
            self.vo.update(frame)
            if self.vo.tracker.frame_idx > 1:
                x = int(self.vo.current_t[0][0])+250
                y = int(self.vo.current_t[2][0])+100
                cv2.circle(self.vo.trajectory, (x, y), 1, (0, 0, 255))
                self.image = self.get_qimage(self.vo.trajectory)
                time.sleep(1/30)
            print(self.vo.tracker.frame_idx)

class MainWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.trajectory_widget = TrajectoryWidget()

    # Create and set the layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.trajectory_widget)


        self.setLayout(layout)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    main_widget = MainWidget()
    main_window.setCentralWidget(main_widget)
    sys.exit(app.exec_())