#! /Users/michael/anaconda3/bin/python
# @Date:   2018-09-29 12:31:04

"""
当该文件对 formdata 的加密有修改时，爬虫需要响应修改：
http://shared.ydstatic.com/fanyi/newweb/v1.0.12/scripts/newweb/fanyi.min.js
"""

import requests
import time
import hashlib
import random

raw_headers = """
Accept: application/json, text/javascript, */*; q=0.01
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7
Cache-Control: no-cache
Connection: keep-alive
Content-Length: 197
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Cookie: OUTFOX_SEARCH_USER_ID_NCOO=2000622643.8010917; DICT_UGC=be3af0da19b5c5e6aa4e17bd8d90b28a|; OUTFOX_SEARCH_USER_ID=-1285637205@183.15.178.61; JSESSIONID=abc4Z6Yaz-IBY_ju9Ntsw; _ntes_nnid=4a354b47eff36739ac6a0fc528835cdd,1531485088595; SESSION_FROM_COOKIE=www.baidu.com; UM_distinctid=16623a37b352e0-0a4bffd278c399-346a7808-13c680-16623a37b3777; ___rl__test__cookies=1538198415404
Host: fanyi.youdao.com
Origin: http://fanyi.youdao.com
Pragma: no-cache
Referer: http://fanyi.youdao.com/
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36
X-Requested-With: XMLHttpRequest
"""

raw_formdata = """
i: {}
from: AUTO
to: AUTO
smartresult: dict
client: fanyideskweb
salt: {}
sign: {}
doctype: json
version: 2.1
keyfrom: fanyi.web
action: FY_BY_REALTIME
typoResult: false
"""

def parse_data(raw_data):
    data = {}
    for line in raw_data.strip().split("\n"):
        k, v = line.split(': ', 1)
        data[k] = v
    return data

def getSalt(): # 得到加盐信息
    return str(int(time.time()*1000)+random.randint(0,10))

def getSign(key, salt):# 得到sign信息
    sign = ("fanyideskweb" + key + salt + "6x(ZHw]mwzX#u0V7@yfwK")
    hashObj = hashlib.md5()
    hashObj.update(sign.encode("utf-8"))
    return hashObj.hexdigest()

def main(key):
    url = "http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"
    headers = parse_data(raw_headers)
    formdata = parse_data(raw_formdata)
    salt = getSalt()
    sign = getSign(key, salt)
    formdata['i'] = key
    formdata['salt'] = int(salt)
    formdata['sign'] = sign
    resp = requests.post(url, headers=headers, data=formdata)
    print(resp.json())

if __name__ == '__main__':

    key = "加油兄弟"
    main(key)













