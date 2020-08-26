# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import *
from core.mainwindow import MainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec_()
