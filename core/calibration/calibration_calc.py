# calibration
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import numpy as np
import cv2
import glob


class calibation:

    def __init__(self, w, l, distance):
        self.chessw_point = w
        self.chessl_point = l
        self.distance = distance

        self.criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        self.objp = np.zeros((self.chessw_point * self.chessl_point, 3), np.float32)
        self.objp[:, :2] = np.mgrid[0:self.chessl_point, 0:self.chessw_point].T.reshape(-1, 2)  # *self.distance

        self.objpoints = []  # 3d point in real world space
        self.imgpoints = []  # 2d points in image plane.

    def calcmatrix(self, locat):
        images = glob.glob(locat)  # 'data4/*.png'
        for fname in images:
            img = cv2.imread(fname)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Find the chess board corners
            ret = False
            ret, corners = cv2.findChessboardCorners(gray, (self.chessl_point, self.chessw_point), None)

            # If found, add object points, image points (after refining them)
            if ret == True:
                self.objpoints.append(self.objp)

                corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), self.criteria)
                self.imgpoints.append(corners2)

                # Draw and display the corners
                img = cv2.drawChessboardCorners(img, (self.chessl_point, self.chessw_point), corners2, ret)
                cv2.imshow('img', img)
                cv2.waitKey(500)

        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(self.objpoints, self.imgpoints, gray.shape[::-1], None, None)
        self.calcerror(ret, mtx, dist, rvecs, tvecs)
        return ret, mtx, dist, rvecs, tvecs

    def Opencv_undistort(self, files, mtx, dist):
        img = cv2.imread(files)
        h, w = img.shape[:2]
        newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
        dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
        x, y, w, h = roi
        dst = dst[y:y + h, x:x + w]
        # filename, _ = QFileDialog.getSaveFileName("Save File", "./test.jpg", "Text files (*.jpg)")
        # if filename:
        cv2.imwrite("./test.jpg", dst)

    def Opencv_initdis(self, files, mtx, dist):

        img = cv2.imread(files)
        h, w = img.shape[:2]
        newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
        mapx, mapy = cv2.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (w, h), 5)
        dst = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)

        # crop the image
        x, y, w, h = roi
        dst = dst[y:y + h, x:x + w]
        # filename, _ = QFileDialog.getSaveFileName("Save File", "./test.jpg", "Text files (*.jpg)")
        # if filename:
        cv2.imwrite("./test2.jpg", dst)

    def calcerror(self, ret, mtx, dist, rvecs, tvecs):
        tot_error = 0
        for i in range(len(self.objpoints)):
            img_points2, _ = cv2.projectPoints(self.objpoints[i], rvecs[i], tvecs[i], mtx, dist)
            error = cv2.norm(self.imgpoints[i], img_points2, cv2.NORM_L2) / len(img_points2)
            tot_error += error
        mean_error = tot_error / len(self.objpoints)
        print("total error: ", tot_error)
        print("mean error: ", mean_error)
