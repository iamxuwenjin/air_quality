# -*- coding: utf-8 -*-
from tianqi.items import TianqiItem
import scrapy


class TqspidersSpider(scrapy.Spider):
    name = 'tqspiders'
    allowed_domains = ['aqistudy.cn']
    base_url = "https://www.aqistudy.cn/historydata/"
    start_urls = [base_url]

    def parse(self, response):
        city_list = response.xpath("//ul/div/li/a/@href").extract()
        city_name = response.xpath("//ul/div/li/a/text()").extract()
        for name,link in zip(city_name,city_list):
            yield scrapy.Request(self.base_url+link, meta={"name":name}, callback=self.month_prase)

    def month_prase(self, response):
        day_link = response.xpath("//tr/td/a/@href").extract()
        print "\n"
        print '请求当天情况'
        for link in day_link:
            yield scrapy.Request(self.base_url+link,meta=response.meta,callback=self.day_prase)

    def day_prase(self, response):
        node_list = response.xpath("//tr")
        print "\n"
        print '分析当天情况——————————'
        node_list.pop(0)
        for node in node_list:
            item = TianqiItem()
            item['city'] = response.meta['name']
            item['date'] = node.xpath("./td[1]/text()").extract_first()
            item['aqi'] = node.xpath("./td[2]/text()").extract_first()
            item['level'] = node.xpath("./td[3]//text()").extract_first()
            item['pm2_5'] = node.xpath("./td[4]/text()").extract_first()
            item['pm10'] = node.xpath("./td[5]/text()").extract_first()
            item['so2'] = node.xpath("./td[6]/text()").extract_first()
            item['co'] = node.xpath("./td[7]/text()").extract_first()
            item['no2'] = node.xpath("./td[8]/text()").extract_first()
            item['o3'] = node.xpath("./td[9]/text()").extract_first()

            yield item

