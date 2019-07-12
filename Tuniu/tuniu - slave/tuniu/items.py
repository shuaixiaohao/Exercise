# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TuniuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection = 'guide'

    title = scrapy.Field()
    imageUrl = scrapy.Field()
    routeDays = scrapy.Field()
    price = scrapy.Field()
    spot_num = scrapy.Field()
    recommend = scrapy.Field()
    travelRoute = scrapy.Field()
    spot = scrapy.Field()
    play = scrapy.Field()
    content = scrapy.Field()


