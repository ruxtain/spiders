#! /Users/michael/anaconda3/bin/python
# @Date:   2018-09-01 15:01:58

# import numpy as np
# import pandas as pd

import pymongo
import os, sys, re
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from settings import MONGO_URI, MONGO_DATABASE, MONGO_COLLECTION

client = pymongo.MongoClient(MONGO_URI)
collection = client[MONGO_DATABASE][MONGO_COLLECTION]

# print(collection.find_one())
# exit(0)
count = 0
for i in collection.find():
    detail = i.get('job_detail')
    id = i.get('positionId')
    salary = i.get('salary')
    if detail and 'flask' in detail:
        count += 1
        print(id, salary)
        print(detail)
        print('\n', '-'*80, '\n')

print(count)