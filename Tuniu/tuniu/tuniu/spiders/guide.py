
import re

from idna import unicode
from scrapy import Selector, Request
from scrapy.spiders import Spider

# from tuniu.items import  TuniuItem
from tuniu.items import  MasterItem


class LianJia(Spider):
    name = 'guide'
    start_urls = ['http://www.tuniu.com/guide/d-zhongguo-40002/jingdian/']
    # 城市列表分页地址
    page_url = 'http://www.tuniu.com/newguide/api/widget/render/?widget=guide.HotDestinationWidget&params%5BpoiId%5D=40002&params%5Bpage%5D='
    # 当前城市玩法的地址
    city_url = 'http://www.tuniu.com/{city}/play-sh-0/'
    # 途牛网址
    tuniu_url = 'http://www.tuniu.com'


    def parse(self, response):
        sel = Selector(response)
        # 获取全部城市的分页数
        page = sel.xpath('//*[@id="list"]/div/ul/@data-pages').extract()[0]
        for i in range(1,int(page) + 1):
            yield Request(self.page_url + str(i), callback=self.parse_city)

    def parse_city(self, response):
        # result = json.loads(response.text)
        # data = result['data']
        sel = Selector(response)
        # 获取每个城市的链接
        href_list = sel.xpath('//li/a[1]/@href').extract()[0:-8]
        for href in href_list:
            city_code = re.findall('/(g[0-9]+)/', href)
            # city_code = href.replace('\\"', '').split('/')
            if city_code:
                yield Request(self.city_url.format(city=city_code[0]), callback=self.parse_play_page, meta={'city':city_code[0]})

    # 当前城市的热门玩法
    def parse_play_page(self, response):
        sel = Selector(response)
        page = sel.xpath('//div[@class="page-bottom"]/a[@rel="nofollow"]').extract()
        for i in range(1, len(page)+1):
            # yield Request(self.city_url.format(city=response.meta.get('city')) + '?page=' + str(i),
            #               callback=self.parse_play)
            item = MasterItem()
            item['url'] = self.city_url.format(city=response.meta.get('city')) + '?page=' + str(i)
            yield item
