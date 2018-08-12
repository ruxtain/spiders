#! /Users/michael/anaconda3/bin/python
# @Date:   2018-08-11 16:53:17
# 京东爬虫：基于 selenium。没有设置无头模式

    
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver

from bs4 import BeautifulSoup
import selenium
import time
import os

DRIVER_PATH = '/usr/local/bin/geckodriver'

class Spider:

    def __init__(self, keyword):
        """
            count: 爬到的产品总数
            complete: 爬取结束信号
        """
        self.driver = webdriver.Firefox(executable_path=DRIVER_PATH)
        self.wait = WebDriverWait(self.driver, timeout=10)
        self.keyword = keyword
        self.count = 0
        self.complete = False

    def search(self):
        self.driver.get('https://www.jd.com/')
        self.wait.until(expected.presence_of_element_located((By.XPATH, '//input[@id="key"]')))
        search_input = self.driver.find_element_by_css_selector('input#key')
        search_input.send_keys(self.keyword)
        search_input.send_keys(Keys.RETURN)
        self.parse()

    def parse(self):
        """
            对产品 item 进行解析，这里仅仅是打印了产品名和图片链接
        """


        self.wait.until(expected.presence_of_element_located((By.XPATH, '//span[@class="fs-tit"]')))
        self.slow_scroll()
        soup = BeautifulSoup(self.driver.page_source, 'lxml')

        if 'disabled' in soup.select('a.pn-next')[0]['class']:
            self.complete = True

        items = soup.select('li.gl-item')
        for item in items:
            self.count += 1
            try:
                image = item.select('div.p-img a img')[0].attrs['src']
            except KeyError:
                image = item.select('div.p-img a img')[0].attrs['data-lazy-img']
            title = item.select('em')[1].text
            print({'id': self.count, 'title': title, 'image': 'http:' + image})


    def slow_scroll(self, seconds=3, pos=7500):
        """
            用 约为 seconds 的时间移动到指定位置, 每次移动 interval 个像素
            ps: 时间移动时间超过 seconds，因为滚动本身也消耗时间
            如果网速非常快，可以设置 seconds = 0
        """
        interval = 350
        times = int(pos/interval) # 移动次数
        current_pos = 0 # 位置
        for i in range(times):
            time.sleep(seconds/times)
            current_pos += interval
            self.driver.execute_script("window.scrollTo(0, {})".format(current_pos))        

    def run_until_complete(self):
        self.search()
        while not self.complete:
            next_page_btn = self.driver.find_element_by_css_selector('a.pn-next')
            next_page_btn.send_keys(Keys.RETURN)
            self.parse()
        print('[结束] 共抓取 {} 个产品信息'.format(self.count))
        self.driver.quit()

if __name__ == '__main__':

    Spider('python cookbook').run_until_complete()













