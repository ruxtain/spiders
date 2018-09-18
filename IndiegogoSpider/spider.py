#! /Users/michael/anaconda3/bin/python
# @Date:   2018-08-31 15:51:04

import os
import asyncio
import aiohttp
import json
import time
import pymongo


def save_to_mongo(content):
    content = json.loads(content)
    try:
        projects = content['response']['discoverables']
    except KeyError:
        print("It's most likely that the scraping is already done.")
        exit(0)
    for project in projects:
        print('saving "%s"' % project['title'])
        try:
            col.insert(project)
        except pymongo.errors.DuplicateKeyError:
            print("It's already done")


async def fetch(page):
    sem = asyncio.Semaphore(10)
    async with sem:
        async with aiohttp.ClientSession() as session:
            while True:
                payload_data["page_num"] = page
                print('fetching page %s' % page)
                async with session.post(url, headers=headers, data=json.dumps(payload_data)) as response:
                    try:
                        content = await response.read()
                        save_to_mongo(content)
                    except aiohttp.client_exceptions.ClientConnectorError:
                        continue                    
                page += 1

                # hit the server gently
                if page % 20 == 0:
                    time.sleep(10)


url = 'https://www.indiegogo.com/private_api/discover'

headers = {
    "referer": "https://www.indiegogo.com/explore/all?project_type=all&project_timing=all&sort=trending",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36",
    "content-type": "application/json;charset=UTF-8",
    "x-csrf-token": "3u0wuVaDjZ7qLnItx6MG5FlRLS1EioG0n2eIaZ+b9LsjbJAOFIvpFUzAKBmQKk2bPSvz9g6zgbdPvyYUSARTZg==",
}

payload_data = {
    "sort": "trending",
    "category_main": None,
    "category_top_level": None,
    "project_timing": None,
    "project_type": None,
    "page_num": None,
    "per_page": 12,
    "q": "",
    "tags": []
}

# Starting Page
page = 1

# Connect to mongo
db = pymongo.MongoClient()['indiegogo']
col = db['col']

# Make sure project_id field has only unique values
col.create_index([("project_id", pymongo.ASCENDING)], unique=True)

# register the event to the loop
future = asyncio.ensure_future(fetch(page))

# let's get started!
loop = asyncio.get_event_loop()
loop.run_until_complete(future)


