#! /Users/michael/anaconda3/bin/python
# @Date:   2018-09-29 12:48:59
# 这边是测试破解的一个地方。。。

import time
import random
import hashlib

def getSalt(): # 得到加盐信息
    return str(int(time.time()*1000)+random.randint(0,11))

def getSign(key,salt):# 得到sign信息
    sign = ("fanyideskweb" + key + salt + "6x(ZHw]mwzX#u0V7@yfwK")
    hashObj = hashlib.md5()
    hashObj.update(sign.encode("utf-8"))
    return hashObj.hexdigest()

'5c50b0943ebeedf47b7da42d8cb2c82e'
getSalt()

key = '测试吗'
salt = '1538197543855'
print(getSign(key, salt))