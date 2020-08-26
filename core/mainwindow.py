# -*- coding: utf-8 -*-

__author__ = "Yu-Sheng Lin"
__copyright__ = "Copyright (C) 2016-2020"
__license__ = "AGPL"
__email__ = "pyquino@gmail.com"

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUi
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
        if self.timer_camera.isActive() == False:
            flag = self.cap.open(self.CAM_NUM)
            if flag == False:
                msg = QMessageBox.warning(self, u"Warning", u"Check for the connector",
                                          buttons=QMessageBox.Ok,
                                          defaultButton=QMessageBox.Ok)
            # if msg==QtGui.QMessageBox.Cancel:
            #                     pass
            else:
                self.timer_camera.start(30)

                # self.button_open_camera.setText(u'Close Camera')
        else:
            self.timer_camera.stop()
            self.cap.release()
            self.label_show_camera.clear()
            # self.button_open_camera.setText(u'Open Camera')

    def show_camera(self):
        flag, self.image = self.cap.read()

        show = cv2.resize(self.image, (640, 480))
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
        self.label_show_camera.setPixmap(QPixmap.fromImage(showImage))

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
