#! /Users/michael/anaconda3/bin/python
# @Date:   2018-08-31 15:51:04

"""

思路:

3个协程函数，2个队列。

init 协程用于初始化 urls_queue 队列
run 协程用于读取 urls_queue 队列并解析新的 url 放入 urls_queue
    如果是页面的大图，则放入 images_queue
fetch_image 协程读取 images_queue，并下载图片

为了不让部分页面的错误响应导致爬虫挂掉，加入了异常处理
为了不爬取重复的 url 和图片，使用了布隆过滤器。

"""

import os
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pybloom import BloomFilter

def parse_urls(soup, response_url):
    """ get urls from soup; return a list """
    for a in soup.find_all('a'):
        url = urljoin(response_url, a.get('href'))
        # 限定 host
        if 'meinv' in url and 'www.tupianzj.com' in url:
            yield url


def parse_images(soup, response_url):
    for img in soup.select('#bigpicimg'):
        url = urljoin(response_url, img['src'])
        yield url


async def fetch_image(images_queue):
    async with aiohttp.ClientSession() as session:
        while True:
            url = await images_queue.get()
            print('下载图片', url)
            try:
                async with session.get(url) as response:
                    content = await response.read()
                    name = os.path.basename(url)
                    with open(os.path.join(root, name), 'wb') as f:
                        f.write(content)
            except aiohttp.client_exceptions.ClientConnectorError:
                continue                    


async def run(urls_queue, images_queue):
    """ 还没有对 url 去重 """
    sem = asyncio.Semaphore(30)
    async with sem:
        async with aiohttp.ClientSession() as session:
            while True:
                url = await urls_queue.get()
                try:
                    print('正在爬取', url)
                    async with session.get(url) as response:
                        response_url = str(response.url)
                        starter.start_urls.remove(url)         # 使之与 urls_queue 同步
                        html = await response.text()
                        soup = BeautifulSoup(html, 'lxml')
                        for url in parse_urls(soup, response_url):
                            if not bloom.add(url):             # 已经存在返回 True, 否则 False
                                starter.start_urls.append(url) # 使之与 urls_queue 同步
                                await urls_queue.put(url)
                        for image in parse_images(soup, response_url):
                            if not bloom.add(image):
                                await images_queue.put(image)
                except aiohttp.client_exceptions.ClientConnectorError:
                    continue
                except aiohttp.client_exceptions.ServerDisconnectedError:
                    continue
                except UnicodeDecodeError:
                    continue


async def init(urls_queue):
    """ 为队列添加第一个链接
    """
    for url in starter.start_urls:
        await urls_queue.put(url)


class Starter:

    """ 
    1. 用于获取起始链接 
    2. __enter__ 返回对象本身，以方便修改内部数据
    3. 临时中断程序的话，会保存队列中的 url 作为下次的 start_urls
    4. 没有考虑直接保存 asyncio.Queue 对象，而是间接通过维护一个列表（Starter.start_urls）实现
    """

    def __init__(self, url_file):
        self.url_file = url_file
        self.start_urls = []

    def __enter__(self):
        if os.path.exists(self.url_file):
            with open(self.url_file, 'r') as f:
                for line in f.readlines():
                    self.start_urls.append(line.strip())
        else:
            self.start_urls = ['http://www.tupianzj.com/meinv/20160727/58975.html']
        return self

    def __exit__(self, *args):
        with open(self.url_file, 'w') as f:
            for line in self.start_urls:
                print(line, file=f)


class Bloom:

    """ 注意 __exit__ 本来应该是任何情况下都运行
    但是在 sublime text 的控制台中，如果使用 KeyboardInterrupt 中断程序，
    它将不会运行，所以最好到命令行运行。

    同时记录最后的 url 和 bloom
    """

    def __init__(self, bloom_file):
        self.bloom_file = bloom_file

    def __enter__(self):
        if os.path.exists(self.bloom_file):
            with open(self.bloom_file, 'rb') as f:
                self.bloom = BloomFilter.fromfile(f)
        else:
            self.bloom = BloomFilter(capacity=10000000, error_rate=0.001)
        return self.bloom

    def __exit__(self, *args):
        with open(self.bloom_file, 'wb') as f:
            self.bloom.tofile(f)


# 储存图片的根目录
root = 'images'
os.makedirs(root, exist_ok=True)

# 布隆过滤器和起始链接的配置
bloom_file = 'spider.bloom'
url_file = 'spider.url'

# 队列建立
urls_queue = asyncio.Queue()
images_queue = asyncio.Queue()

# 注册事件到时间循环
asyncio.ensure_future(init(urls_queue))
asyncio.ensure_future(fetch_image(images_queue))
asyncio.ensure_future(run(urls_queue, images_queue))

# 启动爬虫
with Bloom(bloom_file) as bloom, Starter(url_file) as starter:
    loop = asyncio.get_event_loop()
    loop.run_forever()


