# -*- coding: utf-8 -*-

import sys

from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QMainWindow, QWidget

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('image_window.ui', self)
        self.show()
        
        self.init_ui()
        self.plot()
        
    def init_ui(self):
        # a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # set the layout
        self.display_layout.addWidget(self.toolbar)
        self.display_layout.addWidget(self.canvas)
        
    def plot(self):
        ''' plot some random stuff '''
        # random data
        import cv2

        # instead of ax.hold(False)
        self.figure.clear()

        # create an axis
        #ax = self.figure.add_subplot(111)
        ax = self.figure.add_subplot(2, 2, 1)
        image = cv2.imread("images//1.png")
        ax.imshow(image)

        ax = self.figure.add_subplot(2, 2, 2)
        image = cv2.imread("images//2.png")
        ax.imshow(image)

        ax = self.figure.add_subplot(2, 2, 3)
        image = cv2.imread("images//3.png")
        ax.imshow(image)

        ax = self.figure.add_subplot(2, 2, 4)
        image = cv2.imread("images//4.png")
        ax.imshow(image)

        # refresh canvas
        self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
    
    