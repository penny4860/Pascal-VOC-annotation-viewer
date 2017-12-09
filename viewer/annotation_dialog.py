# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5 import uic
import os

UI_FILENAME = os.path.join(os.path.dirname(__file__),
                           'ui',
                           'AnnotationDialog.ui')

class AnnotationInputDialog(QDialog):
    def __init__(self, parent = None):
        super(AnnotationInputDialog, self).__init__(parent)
        uic.loadUi(UI_FILENAME, self)
        self.cb.addItem("SvhnBoxAnnotation")
        self.cb.addItem("MyBoxAnnotation")
        
        self.btn.clicked.connect(self.close)

    @staticmethod
    def getAnnotation(parent = None):
        dialog = AnnotationInputDialog(parent)
        _ = dialog.exec_()
        ann = dialog.cb.currentText()
        return ann

if __name__ == '__main__':
    app = QApplication([])
    ann = AnnotationInputDialog.getAnnotation()
    print (ann)
