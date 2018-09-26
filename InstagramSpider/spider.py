# Michael Tan 2018.09.26

"""
post 页面 json 解析备份

帖子大图 img_url：
content['graphql']['shortcode_media']['display_url']

帖子喜欢数 like_count：
content['graphql']['shortcode_media']['edge_media_preview_like']['count']

评论数 comment_count：
content['graphql']['shortcode_media']['edge_media_to_comment']['count']

评论列表：
content['graphql']['shortcode_media']['edge_media_to_comment']['edges']

单个评论：
comment = content['graphql']['shortcode_media']['edge_media_to_comment']['edges'][0]

评论内容 text：
omment['node']['text']


page 级别：

j['data']['user']['edge_owner_to_timeline_media']['page_info']

{'has_next_page': True,
 'end_cursor': 'AQBostyNm3-o0WClyuyhoM3S0qVgP4rVidHfMfOZNrhKVTAgP0J3YbC2gDJeuIcvsyGTmAwoZLfRVNm6W5bvK5phhwBc-KvgsvXk2IzeF4IUB0CUgNoF_CAXFZa3cRvQ14A'}
"""

import sys
import asyncio
import aiohttp
import json
import time
import random
import pymongo
import hashlib


def save_to_mongo(item, maximum=120):
    print(item)
    col.insert_one(item.copy())
    if col.count_documents(filter={}) >= maximum:
        print('已经搜集到足够内容')
        sys.exit(0)

def random_sleep():
    time.sleep(random.uniform(1,3))

def parse(content):
    try:
        json_data = json.loads(content)
    except json.JSONDecodeError:
        print('content:', content)
        print('Shit!')
        sys.exit(0)
    comments = json_data['data']['user']['edge_owner_to_timeline_media']['edges']
    item = {}
    for comment in comments:
        item['img_url'] = comment['node']['display_url']
        item['like_count'] = comment['node']['edge_media_preview_like']['count']
        item['comment_count'] = comment['node']['edge_media_preview_comment']['count']
        try:
            item['text'] = comment['node']['edge_media_preview_comment']['edges'][0]['node']['text']
        except IndexError:
            item['text'] = ''

        yield item

    page_info = json_data['data']['user']['edge_owner_to_timeline_media']['page_info']
    if page_info['has_next_page']:
        page = page_info['end_cursor']
        yield page
    else:
        print("已经到了尽头")


def get_ig_gis(id, after, rhx_gis):
    params = '{{"id":"{0}","first":12,"after":"{1}"}}'.format(id, after)
    vals = rhx_gis + ":" + params
    return hashlib.md5(vals.encode('utf-8')).hexdigest()

async def fetch_page(base_url, id, after, rhx_gis):
    async with aiohttp.ClientSession() as session:
        page = 1
        while True:
            print('######### PAGE #{} #########'.format(page))
            page += 1
            random_sleep()

            url = base_url.format(id, after)
            headers['x-instagram-gis'] = get_ig_gis(id, after, rhx_gis)
            async with session.get(url, headers=headers) as response:
                content = await response.text()
                for parsed in parse(content):
                    if isinstance(parsed, dict):
                        save_to_mongo(parsed)
                    else:
                        after = parsed


base_url = 'https://www.instagram.com/graphql/query/?query_hash=a5164aed103f24b03e7b7747a2d94e3c&variables=%7B%22id%22%3A%22{}%22%2C%22first%22%3A12%2C%22after%22%3A%22{}%22%7D'
id = '25025320'
after = 'AQBpJyq4lVlWiBXUzpj1K_bBM4R2UwaA6Q0eiU8xNZOG98BG1QpJksbrdDgrtnnYHEp5zVd1D2SKZNnNkHYqQHlNsFyx5ysSWqbzs5-4BpISspgbIjI7vcsbm4oJ66Gixzk'
rhx_gis = '30aab86d18b507c1fd19a20cae8c4ac4'

headers = {
    'accept': '*/*', 
    'accept-encoding': 'gzip, deflate, br', 
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7', 
    'cache-control': 'no-cache', 
    'pragma': 'no-cache', 
    'referer': 'https://www.instagram.com/instagram/', 
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36', 
    'x-requested-with': 'XMLHttpRequest',
}

# Connect to mongo
db = pymongo.MongoClient()['instagram']
col = db['col']

# register the event to the loop
future = asyncio.ensure_future(fetch_page(base_url, id, after, rhx_gis))

loop = asyncio.get_event_loop()
loop.run_until_complete(future)


