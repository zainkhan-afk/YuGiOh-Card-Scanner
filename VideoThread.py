from PyQt5.QtCore import QThread, pyqtSignal
import numpy as np
import cv2
import time
import glob

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True
        self._pause = False

    def run(self):
        # capture from web cam
        cap = cv2.VideoCapture("20230301_134850.mp4")
        while self._run_flag:
            if not self._pause:
                ret, cv_img = cap.read()
                # cv_img = cv2.rotate(cv_img, cv2.ROTATE_180)
            if ret:
                self.change_pixmap_signal.emit(cv_img)
                time.sleep(0.03)
        # shut down capture system
        cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()

    def pause(self):
        """Sets run flag to False and waits for thread to finish"""
        self._pause = not self._pause