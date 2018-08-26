# -*- coding: utf-8 -*-

# Scrapy settings for LagouSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'LagouSpider'

SPIDER_MODULES = ['LagouSpider.spiders']
NEWSPIDER_MODULE = 'LagouSpider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'LagouSpider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 3

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 2
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# 两个请求对应不同的请求头
INDEX_REQUEST_HEADERS = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://www.lagou.com',
    'Referer': 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',  
    'X-Anit-Forge-Code': '0',
    'X-Anit-Forge-Token': 'None',
    'X-Requested-With': 'XMLHttpRequest',
}

DETAIL_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Host': 'www.lagou.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/68.0.3440.106 Safari/537.36',  
    'Upgrade-Insecure-Requests': '1',
    'Host': 'www.lagou.com',
    'Origin': 'https://www.lagou.com',
    'Referer': 'https://www.lagou.com/',
    'Cookie': 'JSESSIONID=ABAAABAAAFCAAEGBC99154D1A744BD8AD12BA0DEE80F320; '
              'showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; '
              'hasDeliver=0; _ga=GA1.2.1111395267.1516570248; _gid=GA1.2.1409769975.1516570248; '
              'user_trace_token=20180122053048-58e2991f-fef2-11e7-b2dc-525400f775ce; PRE_UTM=; '
              'LGUID=20180122053048-58e29cd9-fef2-11e7-b2dc-525400f775ce; '
              'index_location_city=%E5%85%A8%E5%9B%BD; X_HTTP_TOKEN=7e9c503b9a29e06e6d130f153c562827;'
              ' _gat=1; LGSID=20180122055709-0762fae6-fef6-11e7-b2e0-525400f775ce; PRE_HOST=github.com;'
              ' PRE_SITE=https%3A%2F%2Fgithub.com%2Fconghuaicai%2Fscrapy-spider-templetes; '
              'PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2F4060662.html;'
              ' Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1516569758,1516570249,1516570359,1516571830;'
              ' _putrc=88264D20130653A0; login=true; unick=%E7%94%B0%E5%B2%A9;'
              ' gate_login_token=3426bce7c3aa91eec701c73101f84e2c7ca7b33483e39ba5;'
              ' LGRID=20180122060053-8c9fb52e-fef6-11e7-a59f-5254005c3644; '
              'Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1516572053; '
              'TG-TRACK-CODE=index_navigation; SEARCH_ID=a39c9c98259643d085e917c740303cc7',    
    # 'Cookie':   'JSESSIONID=ABAAABAAAIAACBI3D96E6D6B3F7D9F3E207C0A7BAB25995; '
    #             'user_trace_token=20180826191649-2087cbfa-d7cf-4eaa-aa26-4d79410bcc3b; '
    #             'Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1535282211; '
    #             '_ga=GA1.2.941416926.1535282211; _gid=GA1.2.1715717775.1535282211; '
    #             'LGSID=20180826191650-878bb32e-a921-11e8-b1c1-5254005c3644; '
    #             'PRE_UTM=; PRE_HOST=; PRE_SITE=; '
    #             'PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2F5029146.html; '
    #             'LGUID=20180826191650-878bb6c6-a921-11e8-b1c1-5254005c3644; '
    #             'Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1535282238; '
    #             'LGRID=20180826191717-9788f12c-a921-11e8-b6a0-525400f775ce',
}

# 数据库配置

MONGO_URI = 'mongodb://localhost:27017'
MONGO_DATABASE = 'lagou'
MONGO_COLLECTION = 'jobs'

# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'LagouSpider.middlewares.LagouspiderDownloaderMiddleware': 543,
}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'LagouSpider.pipelines.MongoPipeline': 300,
}


# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'LagouSpider.middlewares.LagouspiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}


# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# 暂时不懂和 download delay 区别
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 1
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
HTTPCACHE_ENABLED = False
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'



# 第三方
RANDOM_UA_TYPE = "random"
