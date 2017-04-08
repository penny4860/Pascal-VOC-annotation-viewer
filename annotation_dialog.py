# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog, QApplication, qApp
from PyQt5 import uic

class DateDialog(QDialog):
    def __init__(self, parent = None):
        super(DateDialog, self).__init__(parent)
        uic.loadUi('AnnotationDialog.ui', self)
        
        self.cb.addItem("SvhnAnnotation")
        self.cb.addItem("MyAnnotation")
        
        self.btn.clicked.connect(qApp.quit)

    def get_annotation(self):
        return self.cb.currentText()

    @staticmethod
    def getAnnotation(parent = None):
        dialog = DateDialog(parent)
        _ = dialog.exec_()
        ann = dialog.cb.currentText()
        return ann

if __name__ == '__main__':
    app = QApplication([])
    ann = DateDialog.getAnnotation()
    print ann
