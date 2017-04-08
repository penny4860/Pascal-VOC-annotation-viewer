

import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QMainWindow, QWidget

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

import random

class Window(QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        # a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to `plot` method
        self.button = QPushButton('Plot')
        self.button.clicked.connect(self.plot)

        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        
        w = QWidget()
        w.setLayout(layout)
        
        self.setCentralWidget(w)

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

    main = Window()
    main.show()

    sys.exit(app.exec_())
