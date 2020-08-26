# -*- coding: utf-8 -*-

__author__ = "Yu-Sheng Lin"
__copyright__ = "Copyright (C) 2016-2020"
__license__ = "AGPL"
__email__ = "pyquino@gmail.com"

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUi
from .show_imageDlg import ShowImageDlg
from .calibation import CalibrationDlg
from time import sleep

import cv2
import cv2.aruco as aruco
import numpy as np


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("core/mainwindow.ui", self)
        self.show()

        self.timer_camera = QTimer()
        self.cap = cv2.VideoCapture()
        self.CAM_NUM = 0
        self.slot_init()
        self.__flag_work = 0
        self.x = 0
        self.count = 0
        self.aruco_flag = False
        self.camera_matrix = None

    def slot_init(self):
        self.button_open_camera.clicked.connect(self.button_open_camera_click)
        self.timer_camera.timeout.connect(self.show_camera)
        self.button_close.clicked.connect(self.close)

    def button_open_camera_click(self):
        self.CAM_NUM = self.camera_num.value()
        if self.timer_camera.isActive() is False:
            flag = self.cap.open(self.CAM_NUM)
            if flag is False:
                msg = QMessageBox.warning(self, u"Warning", u"Check for the connector",
                                          buttons=QMessageBox.Ok,
                                          defaultButton=QMessageBox.Ok)
            else:
                self.timer_camera.start(30)
                # init for the mousePressEvent
                # Check the camera is opened
                self.label_show_camera.mousePressEvent = self.getPos
        else:
            self.timer_camera.stop()
            self.cap.release()
            self.label_show_camera.clear()
            # self.button_open_camera.setText(u'Open Camera')

    def show_camera(self):

        flag, self.image = self.cap.read()
        if self.aruco_flag is True:

            if self.camera_matrix is None:
                error_dialog = QErrorMessage()
                error_dialog.showMessage('Oh no you do not have load the matrix\n'
                                         'Please sure you have clicked the load mtx button\n'
                                         'Program will close in 1 sec\n')
                error_dialog.exec_()
                exit()

            # load the matrix in Camera Matrix
            aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_ARUCO_ORIGINAL)
            parameters = aruco.DetectorParameters_create()

            gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            ret, out1 = cv2.threshold(gray, 90, 255, cv2.THRESH_BINARY)
            corners, ids, rejected = aruco.detectMarkers(image=out1, dictionary=aruco_dict, parameters=parameters,
                                                         cameraMatrix=self.camera_matrix,
                                                         distCoeff=self.camera_distortion)
            if ids is not None:
                # -- Find the marker's 6-DOF pose
                rvecs, tvecs, _objPoints = aruco.estimatePoseSingleMarkers(corners, self.marker_size, self.camera_matrix,
                                                                           self.camera_distortion)
                # print(rvecs)
                for i in range(rvecs.shape[0]):
                    aruco.drawAxis(self.image, self.camera_matrix, self.camera_distortion, rvecs[i, :, :], tvecs[i, :, :], 50)
                    aruco.drawDetectedMarkers(self.image, corners)
                id_str = "id:{}".format(ids[0][0])
                rvecs_str = "rvecs:{:.2f},{:.2f},{:.2f}".format(rvecs[0][0][0], rvecs[0][0][1], rvecs[0][0][2])
                tvecs_str = "tvecs:{:.3f},{:.3f},{:.3f}".format(tvecs[0][0][0], tvecs[0][0][1], tvecs[0][0][2])
                center_point_str = f"center point {corners}"
                cv2.putText(self.image, id_str, (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 5)
                cv2.putText(self.image, rvecs_str, (0, 130), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 5)
                cv2.putText(self.image, tvecs_str, (0, 230), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 5)
                cv2.putText(self.image, center_point_str, (0, 330), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 5)
                self.tvec_label.setText(tvecs_str)
                self.rvec_label.setText(rvecs_str)
        else:
            pass
        # show = cv2.resize(self.image, (640, 480))
        show = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
        self.label_show_camera.setPixmap(QPixmap.fromImage(showImage))
        self.label_show_camera.resize(self.widget.size())
        self.label_show_camera.setScaledContents(True)

    def getPos(self, event):
        x = event.pos().x()
        y = event.pos().y()
        print(self.image.shape)
        print(self.widget.size())
        print(x, y)

    @pyqtSlot()
    def on_capture_image_clicked(self):
        catch_image = self.image
        print(catch_image.shape)
        filename, _ = QFileDialog.getSaveFileName(self, "Save JPG File", "data.jpg", "JPG files (*.jpg)")
        if filename:
            cv2.imwrite(filename, catch_image)
        # imageDlg = ShowImageDlg(catch_image, self.show_camera_scale.value())
        # imageDlg.exec_()
        # select_area = imageDlg.recallposition()
        # print(select_area)

    @pyqtSlot()
    def on_calibration_btn_clicked(self):
        print("calibration")
        dlg2 = CalibrationDlg()
        # dlg2.show()
        dlg2.exec_()

    @pyqtSlot()
    def on_load_calibmtx_btn_clicked(self):
        print("load inner mtx")
        WorkingSpace = "."
        self.camera_matrix = np.loadtxt(WorkingSpace + '/config/CameraMatrix.txt', delimiter=',')
        self.camera_distortion = np.loadtxt(WorkingSpace + '/config/CameraDistortion.txt', delimiter=',')

    @pyqtSlot()
    def on_aruco_class_btn_clicked(self):
        print("classifier ArUco")
        if self.aruco_flag is True:
            self.aruco_flag = False
        else:
            self.aruco_flag = True
        print(self.aruco_flag)

    def closeEvent(self, event):
        ok = QPushButton()
        cacel = QPushButton()
        msg = QMessageBox(QMessageBox.Warning, u"Close", u"Check for close！")
        msg.addButton(ok, QMessageBox.ActionRole)
        msg.addButton(cacel, QMessageBox.RejectRole)
        ok.setText(u'Yes')
        cacel.setText(u'No')
        if msg.exec_() == QMessageBox.RejectRole:
            event.ignore()
        else:
            # self.socket_client.send_command(self.socket_client.current_user_command)
            if self.cap.isOpened():
                self.cap.release()
            if self.timer_camera.isActive():
                self.timer_camera.stop()
            event.accept()

    def classifier_aruco(self, maker_size=141):
        self.maker_size = maker_size
        pass
        # marker_size = 141  # [mm]
        # --- Get the camera calibration path


