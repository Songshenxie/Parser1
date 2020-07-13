import sys
from tkinter.dialog import Dialog

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QDialog, QApplication, QLabel, QProgressBar


class Ui_Dialog(object):


    def initUI(self,QDialog):
        self.dialog = QDialog()
        self.label = QLabel('已经发现多个数据待爬',self)
        self.label.setGeometry(QtCore.QRect(10, 9, 381, 41))
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.progressBar = QProgressBar(self)
        self.progressBar.setGeometry(QtCore.QRect(20, 80, 361, 31))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setTextVisible(True)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.progressBar.setObjectName("progressBar")




    # def retranslateUi(self, Dialog):
    #     _translate = QtCore.QCoreApplication.translate
    #     Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
    #     self.label.setText(_translate("Dialog", "已经发现这么多个数据待爬"))

# if __name__ == '__main__':
#     # 创建应用程序和对象
#     app = QApplication(sys.argv)
#     app.setStyle('Fusion')
#     ex = Ui_Dialog()
#     ex.show()
#     sys.exit(app.exec_())