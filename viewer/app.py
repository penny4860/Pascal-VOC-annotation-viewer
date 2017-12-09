# -*- coding: utf-8 -*-

import sys
import os

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

from viewer.annotation_dialog import AnnotationInputDialog
from viewer.info.model import Model

UI_FILENAME = os.path.join(os.path.dirname(__file__),
                           'ui',
                           'main.ui')

class ImageViewer(QMainWindow):
    def __init__(self):
        super(ImageViewer, self).__init__()
        uic.loadUi(UI_FILENAME, self)
        self.model = Model(self)

        self.show()
        self.init_ui()
        self.setup_signal_slots()

    def init_ui(self):
        # 1. Create FigureCanvas instance
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        # 2. Create toolbar
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
        files, _ = QFileDialog.getOpenFileNames(self,
                                                'Open file',
                                                "",
                                                "Image files (*.png)")

        if files:
            self.model.changed(image_files=files)
        else:
            pass

    def _open_ann_file_dialog(self, ann_kinds):
        filename, _ = QFileDialog.getOpenFileName(self,
                                                  'Open annotation file',
                                                  "",
                                                  "Image files (*.json)")

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
