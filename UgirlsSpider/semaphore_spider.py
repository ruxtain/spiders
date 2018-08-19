#! /Users/michael/anaconda3/bin/python
# @Date:   2018-08-18 19:14:05

# 控制信号量爬取

from bs4 import BeautifulSoup
import threading
import requests
import sys
import os

# 同时运行的请求页面的线程个数
POOL_SIZE = 10
# 同时运行的下载图片的线程个数
DOWNLOAD_SIZE = 3
SAVE_DIR = 'sema-images'
# 翻页上限
PAGE = 50


def download_images(url, semaphore_download):
    with semaphore_download:
        name = os.path.join(SAVE_DIR, os.path.basename(url))
        response = requests.get(url)
        if response.content:
            with open(name, 'wb') as f:
                f.write(response.content)
                print(url, '保存成功！')


def get_image_urls(url, semaphore_pool, semaphore_download):
    with semaphore_pool:
        response = requests.get(url)
        print('获取页面', url)
        soup = BeautifulSoup(response.text, 'lxml')
        imgs = soup.select('div.chao div.yang > img.scaleimg')
        for img in imgs:
            threading.Thread(target=download_images, args=(img['src'], semaphore_download)).start()


if __name__ == '__main__':
    
    os.makedirs(SAVE_DIR, exist_ok=True)
    semaphore_pool = threading.Semaphore(POOL_SIZE)
    semaphore_download = threading.Semaphore(DOWNLOAD_SIZE)

    for i in range(1, PAGE+1):
        url = 'https://www.ugirls.com/Shop/Detail/Product-{:03}.html'.format(i)
        threading.Thread(target=get_image_urls, args=(url, semaphore_pool, semaphore_download)).start()













