#! /Users/michael/anaconda3/bin/python
# @Date:   2018-08-26 22:27:11

import numpy as np
import pandas as pd

import pymongo
import os, sys, re
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from settings import MONGO_URI, MONGO_DATABASE, MONGO_COLLECTION

client = pymongo.MongoClient(MONGO_URI)
collection = client[MONGO_DATABASE][MONGO_COLLECTION]

df = pd.DataFrame(list(collection.find()))


skills_count = {}
for position in collection.find({'skills': {'$exists': 1}}):

    skills = position['skills']

    for skill in skills:
        if skill in skills_count:
            skills_count[skill] += 1
        else:
            skills_count[skill] = 1

sorted_skills_count = sorted(skills_count.items(), key=lambda i:i[1], reverse=True)
for k,v in sorted_skills_count:
    print(k, v)



