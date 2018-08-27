# -*- coding: utf-8 -*-

from LagouSpider.items import PositionItem, DetailItem
from urllib.parse import quote

import scrapy
import json
import re
import time

def get_skills(job_detail):
    """ 返回我所需要的 ascii 字符，具体可以查看 ord 为 1-256 这部分字符 """
    skills = []
    raw_skills = re.findall(r'[\x21-\x7f]+', job_detail)
    for skill in raw_skills:
        skill = re.sub(r'^\W*|\W*$', '', skill)      # 去掉无关字符
        if re.match(r'\d+', skill):                  # 纯数字不要
            continue
        if len(skill) <= 1:                          # 只有一位的不要
            continue

        skill = skill.lower()                        # 不分大小写
        split_skills = re.split(r'[/,]', skill)      # 连在一起的拆开
        if len(split_skills) > 1:
            skills.extend(split_skills)
        else:
            skills.append(skill)
    return skills


class LagouSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']

    def start_requests(self):
        """ 先只爬一页 """

        city = '深圳'
        keyword = '数据分析'
        url = 'https://www.lagou.com/jobs/positionAjax.json?city={}&needAddtionalResult=false'
        for pn in range(1, 10):
            yield scrapy.FormRequest(
                url = url.format(quote(city)),
                formdata = {'first': 'true', 'pn': str(pn), 'kd': keyword},
                callback = self.parse_page,
                dont_filter=True # 链接是一样的，只是 post 的 data 不同，所以不要过滤
            )

    def parse_page(self, response):
        data = json.loads(response.text)
        positions = data['content']['positionResult']['result'] # list obj
        for position in positions:
            item = PositionItem()
            for field in item.fields:
                item[field] = position.get(field) # 只有 job_detail, skills 还没有
            yield item

            positionId = position['positionId']
            url = 'https://www.lagou.com/jobs/{}.html'.format(positionId)
            yield scrapy.Request(
                url = url,
                callback = self.parse_detail,
                meta = {'positionId': positionId} # 不会覆盖默认的 meta，只是增加一个键值对
            )

    def parse_detail(self, response):
        item = DetailItem()
        positionId = response.meta['positionId']
        paragraphs = response.xpath('//dd[@class="job_bt"]/div/p/text()').extract()
        job_detail = '\n'.join(paragraphs)

        item['positionId'] = positionId
        item['job_detail'] = job_detail
        item['skills'] = get_skills(job_detail)

        yield item


        



