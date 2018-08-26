#! /Users/michael/anaconda3/bin/python
# @Date:   2018-08-26 18:09:13

import pymongo

client = pymongo.MongoClient()
col = client['test']['test']
col.update_one({'name': 'Alice'}, {'$set': {'name': 'Alice', 'no': 2, 'age':18}}, upsert=True)