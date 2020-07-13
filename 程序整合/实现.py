
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QDialog
from PyQt5 import QtWidgets
from 程序整合.ChildWindow import Ui_Dialog
from 程序整合 import WebScrawl
import os
import sys
import requests

from 程序整合.WebScrawl import ScrawlThread


class scrawl(QDialog,Ui_Dialog):

    def __init__(self,surl,auto_close=True,parent=None):
        super(scrawl,self).__init__(parent)
        self.initUI(QDialog)
        self.progressBar.setValue(0)
        self.downloadThread = None
        self.surl = surl
        self.auto_close = auto_close
        self.scrawl()

    def scrawl(self):
        self.scrawlThread = ScrawlThread(self.surl)
        self.scrawlThread.scrwal_process_signal.connect(self.change_progressbar_value)
        self.scrawlThread.start()

    def change_progressbar_value(self,value):
        self.progressBar.setValue(value)
        if self.auto_close and value == 100:
            self.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = scrawl('https://www.vanpeople.com/c/list/4.html')
    ui.show()
    sys.exit(app.exec_())