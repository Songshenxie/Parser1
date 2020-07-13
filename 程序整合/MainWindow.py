import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets

from 程序整合 import ChildWindow
from 程序整合.ChildWindow import Ui_Dialog


class MainWindow(QWidget):

    def __init__(self,parent=None):
        super(MainWindow,self).__init__(parent)

        self.initUI()  # 界面绘制交给InitUi方法

    def initUI(self):
        self.resize(500, 420)
        self.center()

        self.setWindowTitle('爬虫器')
        self.setWindowIcon(QIcon('levelGrow_8.png'))

        btn = QPushButton('开始爬虫', self)
        btn.clicked.connect(self.btnClicked)
        btn.resize(btn.sizeHint())
        btn.move(200, 180)


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def btnClicked(self):
        self.child_win = Ui_Dialog()
        self.child_win.show()


if __name__ == '__main__':
    # 创建应用程序和对象
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
