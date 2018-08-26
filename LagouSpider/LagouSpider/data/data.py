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


# skills_count = {}
# for position in collection.find({'skills': {'$exists': 1}}):
#     # print(position['skills'])
#     # position['salary']

#     skills = position['skills']

#     for skill in skills:
#         if skill in skills_count:
#             skills_count[skill] += 1
#         else:
#             skills_count[skill] = 1

# sorted_skills_count = sorted(skills_count.items(), key=lambda i:i[1], reverse=True)
# for k,v in sorted_skills_count:
#     print(k, v)

def parse_salary(raw_salary):
    count = 0
    total = 0
    for num in re.findall(r'\d+', raw_salary):
        count += 1
        total += int(num)
    return (total/count)



df = pd.read_table('rank.tsv', sep=' ', names=['terms', 'frequency'])


mean_salaries = []
for i in df.terms:

    count = 0
    total = 0
    for j in collection.find({'job_detail': {'$regex': r'.*{}.*'.format(i)}}):
        count += 1
        total += parse_salary(j['salary'])

    if count > 0:
        mean_salaries.append(total/count)
    else:
        mean_salaries.append(np.nan)

df['value'] = pd.Series(mean_salaries)
df.sort_values('frequency', ascending=False, inplace=True)
df.to_csv('关键词_Python_根据词频排序.csv')
df.sort_values('value', ascending=False, inplace=True)
df.to_csv('关键词_Python_根据平均薪资排序.csv')
print(df)















