# -*- coding: utf-8 -*-

import sys
import cv2

from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QMainWindow, QWidget, QFileDialog

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt


class Model:
    """
    # Attributes
        image_files : list of strings
    
    """
    def __init__(self, viewer):
        self._viewer = viewer
        self.image_files = []

    def changed(self, image_files=None):
        if image_files:
            self.image_files = image_files

        self.notify_viewer()

    def notify_viewer(self):
        self._viewer.update()
        

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('image_window.ui', self)
        self.model = Model(self)
        
        self.show()
        self.init_ui()
        # self.plot()
        
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
        
        self.actionLoad_images.triggered.connect(self._open_file_dialog)

    
    def _open_file_dialog(self):
        files, _ = QFileDialog.getOpenFileNames(self, 'Open file', "", "Image files (*.png)")
        
        if files:
            self.model.changed(image_files=files)
        else:
            pass
            
        
    def update(self):
        self.figure.clear()
        
        n_rows = 2
        n_cols = 2
        
        for i in range(4):
            filename = self.model.image_files[i]
            
            if filename:
                ax = self.figure.add_subplot(2, 2, i+1)
                image = cv2.imread(filename)
                ax.imshow(image)

        # refresh canvas
        self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
    
    