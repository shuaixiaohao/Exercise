# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import redis


class MasterPipeline(object):
    def __init__(self):
        # 连接redis
        self.r = redis.Redis(host='127.0.0.1', port=6379)

    def process_item(self, item, spider):
        # 向redis中插入需要爬取的链接地址
        self.r.lpush('tuniu:start_urls', item['url'])