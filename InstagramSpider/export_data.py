#! /Users/michael/anaconda3/bin/python
# @Date:   2018-09-26 08:08:10


import pymongo
import json

# Connect to mongo
db = pymongo.MongoClient()['instagram']
col = db['col']

data = []
for item in col.find({}):
    item.pop('_id')
    data.append(item)


res = json.dumps({"data": data})
with open('data.json', 'w', encoding='utf-8') as f:
    print(res, file=f)