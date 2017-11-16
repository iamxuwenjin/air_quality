# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
from selenium import webdriver
import scrapy
import time

class SeleniumMiddleware(object):
    def process_request(self,request,spider):
        if request.url != "https://www.aqistudy.cn/historydata/":
            dr = webdriver.Chrome()
            dr.get(request.url)
            time.sleep(2)
            html = dr.page_source
            dr.quit()
            return scrapy.http.HtmlResponse(url=request.url,body=html.encode("utf-8"),encoding='utf-8',request=request)