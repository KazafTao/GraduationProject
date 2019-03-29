# -*- coding: utf-8 -*-
import scrapy


class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    allowed_domains = ['image.baidu.com']
    start_urls = ['http://image.baidu.com/']

    def parse(self, response):
        pass
