#! /Users/michael/anaconda3/bin/python
# @Date:   2018-08-09 16:08:21
# 线程池爬取尤果网图片

from bs4 import BeautifulSoup
from queue import Queue
import threading
import requests
import time
import sys
import os

# 队列长度
QUEUE_SIZE = 30
# 下图片线程个数
POOL_SIZE = 10
# 翻页上限
PAGE = 50


class MasterThread(threading.Thread):

    """
        不停遍历 URL，返回图片链接到队列 q
    """

    def __init__(self, queue):
        self.queue = queue
        self.base_url = 'https://www.ugirls.com/Shop/Detail/Product-{:03}.html'
        super(MasterThread, self).__init__()

    def run(self):
        for i in range(1, PAGE+1):
            print('正在读取第 {} 页...'.format(i))
            url = self.base_url.format(i)
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'lxml')
            imgs = soup.select('div.chao div.yang > img.scaleimg')
            for img in imgs:
                self.queue.put(img['src'])
        self.queue.join()


class SlaveThread(threading.Thread):

    """
        下载并保存图片
    """

    def __init__(self, queue, master):
        self.queue = queue
        super(SlaveThread, self).__init__()

    def run(self):
        while True:
            url = self.queue.get()
            name = os.path.join('images', os.path.basename(url))
            response = requests.get(url)
            if response.content:
                with open(name, 'wb') as f:
                    f.write(response.content)
                    print(url, '保存成功！')
            self.queue.task_done()


if __name__ == '__main__':
    
    os.makedirs('images', exist_ok=True)
    queue = Queue(QUEUE_SIZE)
    master = MasterThread(queue)
    master.start()

    for i in range(POOL_SIZE):
        slave = SlaveThread(queue, master)
        slave.daemon = True
        slave.start()

