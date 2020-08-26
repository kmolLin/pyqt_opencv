__author__ = "Yu-Sheng Lin"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyquino@gmail.com"

import sys
import numpy as np
import cv2

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5.QtGui import *


class ShowImageDlg(QDialog):

    def __init__(self, image: np.ndarray, scale: int):
        super(ShowImageDlg, self).__init__()
        self.scale = scale
        self.drawing = False
        self.lastPoint = QPoint()
        show = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
        self.image = QPixmap.fromImage(showImage)
        # self.setGeometry(100, 100, 500, 300)
        self.resize(self.image.width() / scale, self.image.height() / scale)
        self.label = QLabel(self)
        self.tmppoint = []
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.image)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos() * self.scale

    def mouseMoveEvent(self, event):
        # this is when for mouse move event
        pass

    def mouseReleaseEvent(self, event):
        painter = QPainter(self.image)
        painter.setPen(QPen(Qt.red, 5, Qt.SolidLine))
        if self.lastPoint == event.pos() * self.scale:
            pass
        else:
            painter.drawRect(QRect(self.lastPoint, event.pos() * self.scale))
            self.update()
            self.tmppoint = [self.lastPoint, event.pos() * self.scale]
            self.close()
        if event.button == Qt.LeftButton:
            self.drawing = False

    def recallposition(self):
        return self.tmppoint


if __name__ == '__main__':
    image_path = "../test1.jpg"
    # dlg = ShowImageDlg("../test1.jpg")
    # dlg.exec_()
    app = QApplication(sys.argv)
    mainMenu = ShowImageDlg(image_path)
    sys.exit(app.exec_())
