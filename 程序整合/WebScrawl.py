
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QDialog
from PyQt5 import QtWidgets
from bs4 import BeautifulSoup

from 程序整合 import ChildWindow
import os
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


# def get_data(html_text):
#     finfo = []
#     bs = BeautifulSoup(html_text, "html.parser")
#     data = bs.find_all('li', {'class': 'g-item f-clear'})
#     for item in data:
#         info = []
#         InnerUrl = []
#         innerurl = ''
#
#         info.append(item.find('a', {'class': 'ahtitle'}).string.strip('\n\r\t": '))
#         # 后面的strip()是为了拔掉无用的字符（html里有意在标题前空了一些格子），如过不加上这一段会出现\r\n\t这些符号
#         info.append(item.find('div', {'class': 'f-fl tel'}).string)
#         info.append(item.find('div', {'class': 'f-fl time'}).string)
#         info.append(item.find('a', {'class': 'ahtitle'}).get('href'))
#
#         InnerUrl.append(item.find('a', {'class': 'ahtitle'}).get('href'))
#
#         innerurl = item.find('a', {'class': 'ahtitle'}).get('href')
#         InnerHtml = get_content(innerurl)
#         bs2 = BeautifulSoup(InnerHtml, "html.parser")
#
#         info.append(bs2.find('h2').string)
#
#         finfo.append(info)
#     return finfo


class ScrawlThread(QThread):

    scrwal_process_signal = pyqtSignal(int)

    def __init__(self,surl):
        super(ScrawlThread,self).__init__()
        self.surl = surl

    def run(self):
        try:
            html = get_content(self.surl)
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
                offset += offset
                process = offset / int(120) * 100
                self.scrwal_process_signal.emit(int(process))

        finally:
            result = finfo

        head = ['标题', '电话', '发布日期', '帖子链接', '物品类别']
        print(result)     #测试看看是否爬成功了
        my_df = pd.DataFrame(result)
        my_df.to_csv('data.csv', index=False, header=head, encoding='utf_8_sig')
        # utf_8_sig这里困扰我好久，写csv文件总是不能识别汉字，全是乱码，现在解决了

