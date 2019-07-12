
import json
import re

from idna import unicode
from scrapy import Selector, Request
from scrapy.spiders import Spider
from scrapy_redis.spiders import RedisSpider

from tuniu.items import TuniuItem


class LianJia(RedisSpider):
    name = 'guide'
    redis_key = 'tuniu:start_urls'
    tuniu_url = 'http://www.tuniu.com'

    # 玩法列表
    def parse(self, response):
        sel = Selector(response)
        play_list = sel.xpath('//ul[@class="thebox clearfix play_warp"]/li')
        for play in play_list:
            play_href = play.xpath('./div[1]/div/a/@href').extract()[0]
            yield Request(self.tuniu_url + play_href, callback=self.parse_play_details)


    # 获取玩法攻略内容
    def parse_play_details(self, response):
        sel = Selector(response)
        item = TuniuItem()
        item['title'] = sel.xpath('//div[@class="brief-title"]/h1/text()').extract()
        item['imageUrl'] = sel.xpath('//*[@id="J_Gallery"]/div/ul/li/img/@src').extract()
        item['routeDays'] = sel.xpath('//div[@class="brief-overview-item"]/strong/text()').extract()[0].strip()
        price = sel.xpath('//div[@class="brief-price-preview"]/span/strong/text()').extract()
        if price:
            item['price'] = '预计花费:' + price[0] + '元'
        spot_num = sel.xpath('/html/body/div[2]/div/div[2]/div[2]/div[4]/div[2]/div[2]/strong/text()').extract()
        if spot_num:
            item['spot_num'] = '游玩景点' + spot_num[0]
        item['recommend'] = sel.xpath('/html/body/div[2]/div/div[2]/div[2]/div[6]/div/div/text()[2]').extract()
        # text = response.text
        # json_text = re.findall('pageData.*?</script>', text, re.S)
        # data = re.findall('window.pageData = (.*?)\n</script>', text, re.S)
        # overview = re.findall('overview(.*)detail', data[0], re.S)
        # to = re.findall('"to":"(.*?)"', overview[0], re.S)

        text_b = response.body  # 获取响应的二进制对象
        text = response.text
        data_b = re.findall(b'window.pageData = (.*?)\n</script>', text_b, re.S)
        data_text = re.findall('window.pageData = (.*?)\n</script>', text, re.S)
        overview = re.findall(b'overview(.*)detail', data_b[0], re.S)  # 整个玩法概览
        to = re.findall(b'"to":"(.*?)"', overview[0], re.S) # 行程地点
        travelRoute_temp = [s.decode("unicode-escape").replace('\\', '') for s in to]
        item['travelRoute'] = []
        # 去掉行程地点列表空字符串
        for i in travelRoute_temp:
            if i:
                item['travelRoute'].append(i)
        spot_items = re.findall(b'"moduleType":1.*?"items".*?"title":"(.*?)"', overview[0], re.S)
        item['spot'] = [s.decode("unicode-escape").replace('\\', '') for s in spot_items] # 景

        play = re.findall(b'"moduleType":6.*?"title":"(.*?)"', overview[0], re.S)
        item['play'] = [s.decode("unicode-escape").replace('\\', '') for s in play] # 玩

        play_detail_text = re.findall('"detail"(.*?)playId:', data_text[0], re.S) # 整个玩法详情
        play_detail_b = re.findall(b'"detail"(.*?)playId:', data_b[0], re.S) # 整个玩法详情
        everday_num = re.findall('"day":([0-9]+),', play_detail_text[0], re.S)
        everday = ['第'+ i + '天' for i in everday_num]
        description = re.findall(b'"description":"(.*?)"',play_detail_b[0], re.S)
        item['content'] = [self.repl(s.decode("unicode-escape")) for s in description]
        yield item


    def repl(self,str):
        str1 = str.replace('\n', '')
        str2 = str1.replace('\u3000', '')
        return str2
