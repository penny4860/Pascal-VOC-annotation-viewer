# -*- coding: utf-8 -*-

import sys
import os
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
        self._image_files = []
        self._first_display_index = 0
        self._ann_truth = None
        self._ann_predict = None

    def changed(self,
                image_files=None,
                index_change=None,
                ann_file_truth=None,
                ann_file_predict=None):
        if image_files:
            self._image_files = image_files
        if index_change:
            self._update_index(index_change)
        if ann_file_truth:
            self._ann_truth = ann_file_truth
        if ann_file_predict:
            self._ann_predict = ann_file_predict

        self.notify_viewer()

    def _update_index(self, amount):
        self._first_display_index += amount
        
        if self._first_display_index < 0:
            self._first_display_index = len(self._image_files) - abs(amount)
        elif self._first_display_index >= len(self._image_files):
            self._first_display_index = 0
            
    def notify_viewer(self):
        self._viewer.update()

    def get_image(self, index):
        """
        # Arguments
            index : int
        
        # Returns
            image : array, shape of (n_rows, n_cols, n_ch)
            filename : str
        """
        if index + self._first_display_index < len(self._image_files):
            filename = self._image_files[index + self._first_display_index]
            image = cv2.imread(filename)
            return image, filename
        else:
            return None, None
        

class ImageViewer(QMainWindow):
    def __init__(self):
        super(ImageViewer, self).__init__()
        uic.loadUi('image_window.ui', self)
        self.model = Model(self)
        
        self.show()
        self.init_ui()
        self.setup_signal_slots()
        
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
        
    def setup_signal_slots(self):
        self.actionLoad_images.triggered.connect(self._open_files_dialog)
        self.sp_n_rows.valueChanged.connect(self._disply_option_changed)
        self.sp_n_cols.valueChanged.connect(self._disply_option_changed)
        self.btn_next.clicked.connect(lambda : self._update_index(self.sp_n_rows.value()*self.sp_n_cols.value()))
        self.btn_back.clicked.connect(lambda : self._update_index(-self.sp_n_rows.value()*self.sp_n_cols.value()))
        self.tb_truth_ann.clicked.connect(lambda : self._open_ann_file_dialog("truth"))
        self.tb_predict_ann.clicked.connect(lambda : self._open_ann_file_dialog("predict"))
        
    def _disply_option_changed(self):
        self.update()
    
    def _update_index(self, amount):
        self.model.changed(index_change=amount)
    
    def _open_files_dialog(self):
        files, _ = QFileDialog.getOpenFileNames(self, 'Open file', "", "Image files (*.png)")
        
        if files:
            self.model.changed(image_files=files)
        else:
            pass

    def _open_ann_file_dialog(self, ann_kinds):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open annotation file', "", "Image files (*.json)")
        
        if filename:
            if ann_kinds == "truth":
                self.model.changed(ann_file_truth=filename)
            elif ann_kinds == "predict":
                self.model.changed(ann_file_predict=filename)
        else:
            pass

    def update(self):
        self.figure.clear()
        
        n_rows = self.sp_n_rows.value()
        n_cols = self.sp_n_cols.value()
        
        for i in range(n_rows * n_cols):
            image, filename = self.model.get_image(i)
            
            if filename:
                ax = self.figure.add_subplot(n_rows, n_cols, i+1)
                ax.imshow(image)
                ax.set_title(os.path.basename(filename))

        # refresh canvas
        self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageViewer()
    sys.exit(app.exec_())
    
    