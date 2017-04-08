# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog, QApplication, qApp
from PyQt5 import uic

class AnnotationInputDialog(QDialog):
    def __init__(self, parent = None):
        super(AnnotationInputDialog, self).__init__(parent)
        uic.loadUi('AnnotationDialog.ui', self)
        
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
    print ann
