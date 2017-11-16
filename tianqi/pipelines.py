# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import CsvItemExporter
from datetime import datetime
import pymongo
import redis
import json


class TianqiPipeline(object):
    def process_item(self, item, spider):
        item['source'] = spider.name
        item['utc_time'] = str(datetime.utcnow())
        return item

class TianqiJsonPipeline(object):
    def open_spider(self,spider):
        self.filename = open("tianqi.json",'wb')

    def process_item(self,item, spider):
        print '准备写入——————'
        content = json.dumps(dict(item))+"\n"
        self.filename.write(content)
        return item

    def close_spider(self,spider):
        self.filename.close()

class TianqiCsvPipeline(object):
    def open_spider(self,spider):
        self.filename = open('tianqi.csv','w')
        self.csv_exporter = CsvItemExporter(self.filename)
        self.csv_exporter.start_exporting()

    def process_item(self,item,spider):
        self.csv_exporter.export_item(item)
        return item

    def close_spider(self,spider):
        self.csv_exporter.finish_exporting()
        self.filename.close()

class TianqiMongoPipeline(object):
    def open_spider(self,spider):
        self.client = pymongo.MongoClient(host="127.0.0.1",port=27017)
        self.db = self.client['tianqi']
        self.collection = self.db["tianqi_data"]

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

class TianqiRedisPipeline(object):
    def open_spider(self,spier):
        self.client = redis.Redis(host="127.0.0.1",port=6379)

    def process_item(self, item,spider):
        content = json.dumps(dict(item))
        self.client.lpush("AQI_ITEM", content)
        return item