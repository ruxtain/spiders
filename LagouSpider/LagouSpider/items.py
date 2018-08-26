# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# 同一批数据分两个，毕竟是来自不同的请求
# 之后 pipeline 处理的时候合并

class PositionItem(scrapy.Item):
    """ 和 json 中的键名保持一致 
    """
    positionId = scrapy.Field()                 # 相当于主键
    positionName = scrapy.Field()               # 职位名称
    salary = scrapy.Field()                     # 工资
    workYear = scrapy.Field()                   # 工作年限要求
    education = scrapy.Field()                  # 教育水平
    city = scrapy.Field()                       # 城市，确保是深圳
    district = scrapy.Field()                   # 辖区，如“南山”
    stationname = scrapy.Field()                # 地铁站
    businessZones = scrapy.Field()              # 商区
    companyFullName = scrapy.Field()            # 公司全名
    companyShortName = scrapy.Field()           # 公司简称
    firstType = scrapy.Field()                  # 职位类别
    secondType = scrapy.Field()                 # 细分
    industryField = scrapy.Field()              # 公司行业
    positionLables = scrapy.Field()             # 职位标签
    createTime = scrapy.Field()                 # 招聘信息创建时间
    lastLogin = scrapy.Field()                  # 最近一次登录


class DetailItem(scrapy.Item):
    positionId = scrapy.Field()                 # 相当于主键
    job_detail = scrapy.Field()                 # 来自详情页的原始信息
    skills = scrapy.Field()                     # 根据详情页进行解析，获取技术名词



