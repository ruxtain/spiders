from subprocess import Popen, PIPE
from queue import Queue
import subprocess
import threading
import settings
import android

import requests
import time
import os
import re

"""
    基本思路：
    三个线程
    一个翻页，以触发服务器的输出，
    一个读取服务器输出（阻塞），在没有输出时，会阻塞；有合适输出，则放入队列
    一个下载队列里的链接

    配置：
    都在 settings.py 文件中。

    使用方法：
    adb 连接手机，启动抖音。
    电脑启动 anyproxy 同时确保其可以对手机抓包

    其他：
    程序勉强能用，爬取速度很慢。
    对于分辨率不同的手机，可能需要修改 settings.py
    测试过的是分辨率是： 2560x1440
"""


class ProxyThread(threading.Thread):

    def __init__(self, queue):
        self.queue = queue
        super().__init__()

    def start(self):
        print('[P] 启动服务器...')
        self.server = subprocess.Popen(['anyproxy', '--intercept'], stdout=subprocess.PIPE)
        time.sleep(5)
        super().start()

    def run(self):
        while self.server.poll() is None:
            line = self.server.stdout.readline().decode('utf-8')
            url = re.findall(r'received request to: GET (.*?ixigua.*?)\n', line)
            if settings.debug:
                print('[P]', line, end='')
            if url:
                url = 'http://' + url[0]
                print('[P] 获取 URL 成功：', url)
                self.queue.put(url)


class SwipeThread(threading.Thread):
    
    def __init__(self, proxy):
        self.proxy = proxy
        self.count = 0
        super().__init__()
        
    def run(self):
        adb = android.Android()
        while self.proxy.is_alive():
            time.sleep(3)
            self.count += 1
            print('[S] 翻第 {} 页'.format(self.count))
            adb.swipe_up()


class DownloadThread(threading.Thread):

    def __init__(self, queue):
        self.queue = queue
        super().__init__()

    def get_download_path(self):
        download_path = 'downloads'
        os.makedirs(download_path, exist_ok=True)
        return download_path

    def run(self):
        while True:
            url = self.queue.get()
            response = requests.get(url=url, headers=settings.headers)
            if response.status_code == 200:
                filename = os.path.basename(url.rstrip('/')) + '.mp4'
                filepath = os.path.join(self.get_download_path(), filename)
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                    print('[D] 视频保存成功', filename)
            self.queue.task_done()


if __name__ == '__main__':
    queue = Queue(30)
    t1 = ProxyThread(queue)
    t2 = SwipeThread(t1)
    t3 = DownloadThread(queue)
    t1.start()
    t2.start()
    t3.start()
    queue.join()







