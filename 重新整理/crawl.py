from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QWidget, QPushButton, QDesktopWidget, QMessageBox
from PyQt5 import QtWidgets, QtGui
from 重新整理.Ui_crawler import Ui_crawler
from bs4 import BeautifulSoup
import sys
import requests
import random
import time
import socket
import http.client
import pandas as pd


def get_content(url, data=None):
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.235'
    }
    timeout = random.choice(range(80, 180))
    while True:
        try:
            rep = requests.get(url, headers=header, timeout=timeout)
            rep.encoding = 'utf-8'
            # req = urllib.request.Request(url, data, header)
            # response = urllib.request.urlopen(req, timeout=timeout)
            # html1 = response.read().decode('UTF-8', errors='ignore')
            # response.close()
            break
        # except urllib.request.HTTPError as e:
        #         print( '1:', e)
        #         time.sleep(random.choice(range(5, 10)))
        #
        # except urllib.request.URLError as e:
        #     print( '2:', e)
        #     time.sleep(random.choice(range(5, 10)))
        except socket.timeout as e:
            print('3:', e)
            time.sleep(random.choice(range(8, 15)))

        except socket.error as e:
            print('4:', e)
            time.sleep(random.choice(range(20, 60)))

        except http.client.BadStatusLine as e:
            print('5:', e)
            time.sleep(random.choice(range(30, 80)))

        except http.client.IncompleteRead as e:
            print('6:', e)
            time.sleep(random.choice(range(5, 15)))

    return rep.text
    # return html_text



class crawlThread(QThread):

    crawl_progress_signal = pyqtSignal(int)

    def __init__(self,scrawl_url,listsize):
        super(crawlThread, self).__init__()
        self.scrawl_url = scrawl_url
        self.listsize = listsize

    def run(self):
        try:
            html = get_content(self.scrawl_url)
            finfo = []
            bs = BeautifulSoup(html, "html.parser")
            data = bs.find_all('li', {'class': 'g-item f-clear'})
            offset = 0
            for item in data:
                info = []
                InnerUrl = []
                innerurl = ''

                info.append(item.find('a', {'class': 'ahtitle'}).string.strip('\n\r\t": '))
                # 后面的strip()是为了拔掉无用的字符（html里有意在标题前空了一些格子），如过不加上这一段会出现\r\n\t这些符号
                info.append(item.find('div', {'class': 'f-fl tel'}).string)
                info.append(item.find('div', {'class': 'f-fl time'}).string)
                info.append(item.find('a', {'class': 'ahtitle'}).get('href'))
                InnerUrl.append(item.find('a', {'class': 'ahtitle'}).get('href'))
                innerurl = item.find('a', {'class': 'ahtitle'}).get('href')
                InnerHtml = get_content(innerurl)
                bs2 = BeautifulSoup(InnerHtml, "html.parser")
                info.append(bs2.find('h2').string)
                finfo.append(info)
                offset = offset + 1.0
                process = (offset / self.listsize) * 100
                self.crawl_progress_signal.emit(int(process))

        finally:
            result = finfo

        head = ['标题', '电话', '发布日期', '帖子链接', '物品类别']
        # print(result)  # 测试看看是否爬成功了
        my_df = pd.DataFrame(result)
        my_df.to_csv('data.csv', index=False, header=head, encoding='utf_8_sig')
        # utf_8_sig这里困扰我好久，写csv文件总是不能识别汉字，全是乱码，现在解决了


class crawl(QDialog, Ui_crawler):

    def __init__(self, crawl_url, auto_close=True, parent=None):
        super(crawl, self).__init__(parent)
        self.setupUi(self)
        self.progressBar.setValue(0)
        self.crawlThread = None
        self.crawl_url = crawl_url
        self.listsize = None
        self.auto_close = auto_close
        self.crawl()

    def crawl(self):
        self.listsize = len(BeautifulSoup(get_content(self.crawl_url),"html.parser").find_all('li', {'class': 'g-item f-clear'}))
        self.crawlThread = crawlThread(self.crawl_url,self.listsize)
        self.crawlThread.crawl_progress_signal.connect(self.change_progressbar_value)
        self.crawlThread.start()

    def change_progressbar_value(self,value):
        self.progressBar.setValue(value)
        if self.auto_close and value == 100:
            self.close()
            self.message()

    def message(self):
        QMessageBox.information(self,"已完成","爬虫结束，可关闭窗口")

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = "爬虫工具"
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 200
        self.initUI()
        self.center()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QIcon('levelGrow_8.png'))
        """在窗体内创建button对象"""
        button = QPushButton("开始爬虫！", self)
        """方法setToolTip在用户将鼠标停留在按钮上时显示的消息"""
        button.setToolTip("点击开始爬虫")
        """按钮坐标x = 100, y = 70"""
        button.move(100, 70)
        """按钮与鼠标点击事件相关联"""
        button.clicked.connect(self.on_click)

        self.show()

    def center(self):
            # 获得主窗口所在的框架
        qr = self.frameGeometry()
            # 获取显示器的分辨率，然后得到屏幕中间点的位置
        cp = QDesktopWidget().availableGeometry().center()
            # 然后把主窗口框架的中心点放置到屏幕的中心位置
        qr.moveCenter(cp)
            # 然后通过 move 函数把主窗口的左上角移动到其框架的左上角
        self.move(qr.topLeft())


    """创建鼠标点击事件"""

    @pyqtSlot()
    def on_click(self):
        self.ui = crawl('https://www.vanpeople.com/c/list/4.html')
        self.ui.show()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = App()
    sys.exit(app.exec_())