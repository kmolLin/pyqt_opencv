# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog

from .calibration.calibration_calc import calibation
from PyQt5.uic import loadUi

import numpy as np


class CalibrationDlg(QDialog):
    """
    calc the matrix
    """
    def __init__(self, parent=None):
        super(CalibrationDlg, self).__init__(parent)
        loadUi("core/calibation.ui", self)
        self.show()

    @pyqtSlot()
    def on_calibation_clicked(self):
        self.w = self.chessew.value()
        self.l = self.chessel.value()
        self.distance = self.chessboard_dis.value()
        self.locate = self.imagePath.text()
        self.locate = f"{self.imagePath.text()}/*.jpg"
        print(self.locate)
        print(self.l)
        print(self.w)

        self.calb = calibation(self.w, self.l, self.distance)
        self.ret, self.mtx, self.dist, self.rvecs, self.tvecs = self.calb.calcmatrix(self.locate)
        print(self.ret, self.mtx, self.dist)
        # TODO: need to calc

    @pyqtSlot()
    def on_undistort_clicked(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Save File", ".calibation_data/data.jpg", "Text files (*.jpg)")
        if filename:
            self.calb.Opencv_undistort(filename, self.mtx, self.dist)

    @pyqtSlot()
    def on_initundistort_clicked(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Save File", ".calibation_data/data.jpg", "Text files (*.jpg)")
        if filename:
            self.calb.Opencv_initdis(filename, self.mtx, self.dist)

    @pyqtSlot()
    def on_imagePbtn_clicked(self):
        dir = QFileDialog.getExistingDirectory(self, "Save File", ".calibation_data/data.jpg", QFileDialog.ShowDirsOnly)
        if dir:
            self.imagePath.insert(dir)

    @pyqtSlot()
    def on_exportmatrix_clicked(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save File", "./test.txt", "Text files (*.txt)")
        if filename:
            # data = []
            # data.append(self.mtx)
            # data.append(self.dist)
            # with open(filename, 'w') as f:
            #     f.write(str(data))
            FileName = "./config/CameraMatrix.txt"
            np.savetxt(FileName, self.mtx, delimiter=',')
            FileName = "./config/CameraDistortion.txt"
            np.savetxt(FileName, self.dist, delimiter=',')