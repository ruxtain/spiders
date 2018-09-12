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


def skill_counter():
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


def find_the_reason():
    count_nanshan = 0
    count_baoan = 0
    for i in collection.find({'job_detail': {"$regex": "实习"}}):
        district = i.get('district')
        if district:
            if '南山' in district:
                count_nanshan += 1
            elif '宝安' in district:
                count_baoan += 1
    print('南山区实习岗位：{}个'.format(count_nanshan))
    print('宝安区实习岗位：{}个'.format(count_baoan))


def intern_pay():
    for i in collection.find({'job_detail': {"$regex": "实习"}}):
        district = i.get('district')
        if district:
            if '南山' in district:
                print(i['salary'])



if __name__ == '__main__':
    intern_pay()
















