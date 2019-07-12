# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import redis
from scrapy.conf import settings

from tuniu.items import TuniuItem


class TuniuPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):
    def __init__(self):
        conn = pymongo.MongoClient(host=settings['MONGODB_HOST'],
                                   port=settings['MONGODB_PORT'])
        db = conn[settings['MONGODB_DB']]
        self.collection = db[TuniuItem.collection]

    def process_item(self, item, spider):
        if isinstance(item, TuniuItem):
            self.collection.update({'title': item.get('title')}, {'$set': item}, True)
            return item


# class MasterPipeline(object):
#     def __init__(self):
#         # 链接redis
#         self.r = redis.Redis(host='127.0.0.1', port=6379)
#
#     def process_item(self, item, spider):
#         # 向redis中插入需要爬取的链接地址
#         self.r.lpush('tuniu:start_urls', item['url'])