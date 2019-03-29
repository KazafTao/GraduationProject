# -*- coding: utf-8 -*-
import scrapy
from fake_useragent import UserAgent
from Crawler.items import EmojiSeriesItem, SeriesElementItem

ua = UserAgent()


# from scrapy_splash import SplashRequest

class SetSpider(scrapy.Spider):
    name = 'set'
    baseurl = 'http://www.doutula.com/article/list/?page='
    page = 12
    max_page = 50
    start_urls = [baseurl + str(page)]

    # 设置假UA
    def __init__(self, **kwargs):
        self.headers = {
            'User-Agent': ua.random,
        }

    # 获取一页中所有系列的名称和url地址
    def parse(self, response):
        # 获取一页中所有系列
        node_list = response.xpath("//div[@class='col-sm-9']/a")
        for node in node_list:
            # 存入item
            item = EmojiSeriesItem()
            item['name'] = node.xpath("./div[@class='random_title']/text()").extract()[0]
            item['url'] = node.xpath("./@href").extract()[0]
            request = scrapy.Request(item['url'], callback=self.getElementUrls,
                                     dont_filter=True, headers=self.headers)
            request.meta['series'] = item
            yield request

        # 翻页
        if self.page <= self.max_page:
            self.page += 1
            yield scrapy.Request(self.baseurl + str(self.page),
                                 callback=self.parse, headers=self.headers)

    def getElementUrls(self, response):
        series = response.meta['series']
        urls = response.xpath("//div[@class='artile_des']//a/img/@onerror").extract()
        series['num'] = 1
        series['path'] = ''
        if isinstance(series, EmojiSeriesItem):
            yield series
        for url in urls:
            element = SeriesElementItem()
            element['series'] = series
            element['url'] = url[10:-1]
            element['path'] = ''
            if isinstance(element, SeriesElementItem):
                yield element
