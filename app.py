# -*- coding: utf-8 -*-

import sys
import os
import cv2

from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QMainWindow, QWidget, QFileDialog

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

from single_shot.annotation import AnnotationLoader
from single_shot.viewer.annotation_dialog import AnnotationInputDialog
from single_shot.annotation import SvhnBoxAnnotation, MyBoxAnnotation


class Model:
    """
    # Attributes
        image_files : list of strings
    
    """
    def __init__(self, viewer):
        self._viewer = viewer
        self._image_files = []
        self._first_display_index = 0
        
        self._list_true_boxes = None
        self._list_predict_boxes = None
        
        self.ann_file_truth = None
        self.ann_file_predict = None

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
            self._list_true_boxes = self._update_annotation(ann_file_truth[0], ann_file_truth[1])
            self.ann_file_truth = ann_file_truth[0]
        if ann_file_predict:
            self._list_predict_boxes = self._update_annotation(ann_file_predict[0], ann_file_predict[1])
            self.ann_file_predict = ann_file_predict[0]

        self.notify_viewer()

    def _update_annotation(self, ann_file, ann_type):
        if ann_type == "SvhnBoxAnnotation":
            box_annotation = SvhnBoxAnnotation()
        elif ann_type == "MyBoxAnnotation":
            box_annotation = MyBoxAnnotation()
        else:
            raise ValueError, "Invalid Annotation type"
        
        ann_loader = AnnotationLoader(ann_file, box_annotation)
        list_boxes = ann_loader.get_list_of_boxes()
        return list_boxes
        
    def _update_index(self, amount):
        self._first_display_index += amount
        
        if self._first_display_index < 0:
            self._first_display_index = len(self._image_files) - abs(amount)
        elif self._first_display_index >= len(self._image_files):
            self._first_display_index = 0
            
    def notify_viewer(self):
        self._viewer.update()

    def get_image(self, index, plot_true_box, plot_predict_box):
        """
        # Arguments
            index : int
            plot_true_box : bool
            plot_predict_box : bool
        
        # Returns
            image : array, shape of (n_rows, n_cols, n_ch)
            filename : str
        """
        if index + self._first_display_index < len(self._image_files):
            filename = self._image_files[index + self._first_display_index]

            image = cv2.imread(filename)
            
            if plot_true_box and self._list_true_boxes:
                boxes = self._list_true_boxes[index + self._first_display_index]
                self._draw_box(image, boxes, (255, 0, 0))
            if plot_predict_box and self._list_predict_boxes:
                boxes = self._list_predict_boxes[index + self._first_display_index]
                self._draw_box(image, boxes, (0, 0, 255))
            return image, filename
        else:
            return None, None

    def _draw_box(self, image, boxes, color):
        """image 에 bounding boxes 를 그리는 함수.

        # Arguments
            image : array, shape of (n_rows, n_cols, n_ch)
            boxes : Boxes instance
            color : tuple, (Red, Green, Blue)
        """
        np_boxes = boxes.get_pos(["x1", "y1", "x2", "y2"])
        for np_box in np_boxes:
            x1, y1, x2, y2 = np_box
            cv2.rectangle(image, (x1, y1), (x2, y2), color, 1)
        

class ImageViewer(QMainWindow):
    def __init__(self):
        super(ImageViewer, self).__init__()
        uic.loadUi('image_window.ui', self)
        self.model = Model(self)
        
        self.show()
        self.init_ui()
        self.setup_signal_slots()
        
    def init_ui(self):
        # 1. FigureCanvas instance 생성
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        
        # 2. toolbar 생성
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
        self.cb_plot_truth_box.stateChanged.connect(self._disply_option_changed)
        self.cb_plot_predict_box.stateChanged.connect(self._disply_option_changed)

        
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
            # message box 를 띄워서 annotation type 을 선택
            annotaion_type = AnnotationInputDialog.getAnnotation(parent=None)
            
            if ann_kinds == "truth":
                self.model.changed(ann_file_truth=(filename, annotaion_type))
            elif ann_kinds == "predict":
                self.model.changed(ann_file_predict=(filename, annotaion_type))
        else:
            pass

    def update(self):
        self.figure.clear()
        
        n_rows = self.sp_n_rows.value()
        n_cols = self.sp_n_cols.value()

        for i in range(n_rows * n_cols):
            image, filename = self.model.get_image(i,
                                                   self._is_cb_checked(self.cb_plot_truth_box),
                                                   self._is_cb_checked(self.cb_plot_predict_box))
            if filename:
                ax = self.figure.add_subplot(n_rows, n_cols, i+1)
                ax.imshow(image)
                ax.set_title(os.path.basename(filename))
        # refresh canvas
        self.canvas.draw()

        self.te_truth_ann.setText(self.model.ann_file_truth)
        self.te_predict_ann.setText(self.model.ann_file_predict)
    
    def _is_cb_checked(self, cb):
        is_checked = True if cb.checkState() > 0 else False
        return is_checked


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageViewer()
    sys.exit(app.exec_())
    
    