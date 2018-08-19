#! /Users/michael/anaconda3/bin/python
# @Date:   2018-08-18 09:34:49
# 协程下载
# 当需要下载的页面叫多，对方服务器会出现阻塞，暂未找到合适解决办法。

from urllib.parse import urljoin
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import os

base_url = 'https://www.ugirls.com/Shop/Detail/Product-{:03}.html'

root = 'coro-images'
os.makedirs(root, exist_ok=True)
loop = asyncio.get_event_loop()


async def get_page(url, semaphore):
    async with semaphore:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                print('获取页面', url)
                text = await response.text()
                soup = BeautifulSoup(text, 'lxml')
                imgs = soup.select('div.chao div.yang > img.scaleimg')
                for img in imgs:
                    image_url = urljoin(base_url, img['src'])
                    await get_image(image_url, semaphore)


async def get_image(image_url, semaphore):
    async with semaphore:
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as response:
                content = await response.read()
                name = os.path.basename(image_url)
                with open(os.path.join(root, name), 'wb') as f:
                    f.write(content)
                    print('下载图片', image_url)

# Mac's `ulimit -a` tells me it can only handle 256 file descriptors
semaphore = asyncio.Semaphore(100) 
tasks = [get_page(base_url.format(i), semaphore) for i in range(1, 100)]
loop.run_until_complete(asyncio.wait(tasks))
