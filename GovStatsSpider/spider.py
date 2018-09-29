#! /Users/michael/anaconda3/bin/python
# @Date:   2018-09-29 12:28:34

import requests
import time
import pandas as pd 
from urllib.parse import urlencode

raw_headers = """
Accept: application/json, text/javascript, */*; q=0.01
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7
Cache-Control: no-cache
Connection: keep-alive
Host: data.stats.gov.cn
Pragma: no-cache
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36
X-Requested-With: XMLHttpRequest
"""

qs = {
        'm': 'QueryData', 
        'dbcode': 'csyd', 
        'rowcode': 'reg', 
        'colcode': 'sj', 
        'wds': '[{"wdcode":"zb","valuecode":"A010101"}]', 
        'dfwds': '', 
        'k1': '',
    }

class Month:

    def __init__(self, year, month):
        self.year = int(year)
        self.month = int(month)

    def add_one(self):
        """ 往后一个月 """
        if self.month == 12:
            self.month = 1
            self.year += 1
        else:
            self.month +=1

    def __lt__(self, other):
        if self.year < other.year:
            return True
        elif self.year > other.year:
            return False
        else:
            return self.month <= other.month

    def __eq__(self, other):
        return self.year == other.year and self.month == other.month

    def __str__(self):
        return '{}{:02d}'.format(self.year, self.month)

    @property
    def name(self):
        return '{}年{:02d}月'.format(self.year, self.month)

def get_months(start, end):
    '''
    根据形如 201711, 201801 的输入，得到所有中间月份：
        201711,201712,201801
    '''
    start, end = str(start), str(end)
    start = Month(start[:4], start[4:])
    end = Month(end[:4], end[4:])

    while start < end:
        yield start
        start.add_one()

def parse_data(raw_data):
    data = {}
    for line in raw_data.strip().split("\n"):
        k, v = line.split(': ', 1)
        data[k] = v
    return data

def get_json_by_month(month):
    qs["dfwds"] = '[{"wdcode":"sj","valuecode":"%s"}]' % str(month)
    qs["k1"] = str(int(1000*time.time()))
    url = "http://data.stats.gov.cn/easyquery.htm?" + urlencode(qs)
    resp = requests.get(url, headers=parse_data(raw_headers))
    return resp.json()

def get_data_by_json(json_data):
    city_data = {}
    for i in range(70):
        city = json_data['returndata']['wdnodes'][1]['nodes'][i]['cname']
        data = json_data['returndata']['datanodes'][i]['data']['data']
        city_data[city] = data
    return city_data

def get_csv_by_date(start, end):
    """
    start:  201701
    end:    201809
    return 表格
    """
    city_datas = []
    columns = []
    for month in get_months(start, end):
        print('正在获取 {} 数据...'.format(month))
        json_data = get_json_by_month(month)
        city_data = get_data_by_json(json_data)
        city_datas.append(city_data)
        columns.append(month.name)

    csv = '主要城市月度价格数据({}-{}).csv'.format(start, end)
    df = pd.DataFrame(city_datas).T
    df.columns = columns # 给每个月份标上中文
    df.to_csv(csv, encoding='utf-8')
    print(csv, '已经就绪。')


if __name__ == '__main__':
    """
        用类似 201701,201812 的格式输入，稍等片刻即可获得数据
        如有乱码，请设置好 csv 的读取编码
    """
    get_csv_by_date(201401, 201801)

