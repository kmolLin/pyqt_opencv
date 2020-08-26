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
from time import sleep

import cv2


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
