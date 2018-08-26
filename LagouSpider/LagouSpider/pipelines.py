# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymongo

class MongoPipeline(object):

    def __init__(self, mongo_uri, mongo_db, mongo_collection):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_collection = mongo_collection

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE'),
            mongo_collection=crawler.settings.get('MONGO_COLLECTION')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.mongo_collection]
        # try:
        #     self.db.create_collection(self.mongo_collection)
        # except pymongo.errors.CollectionInvalid:
        #     pass

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):

        item_name = item.__class__.__name__
        item = dict(item)

        if item_name == 'PositionItem':
            self.collection.update_one(
                {'positionId': item['positionId']},
                {'$set': item}, 
                upsert=True
            )

        elif item_name == 'DetailItem':
            """ 找到 PositionItem 存储的 Doucment 然后更新
                不创建新条目，upsert 保持默认值 False
            """
            self.collection.update_one({'positionId':item['positionId']}, {'$set': item})






















