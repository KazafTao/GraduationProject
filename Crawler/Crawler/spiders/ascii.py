# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

from Crawler.items import AsciiEmojiItem, TagItem


class AsciiSpider(scrapy.Spider):
    name = 'ascii'
    allowed_domains = ['facemood.grtimed.com']
    baseurl = 'http://facemood.grtimed.com/?search='
    tags = []
    count = 0

    with open("E:/GraduationProject/Crawler/Crawler/datas/final.txt", "r", encoding='utf-8') as f:
        for tag in f.readlines():
            tag = tag.strip()
            if tag:
                tags.append(tag)

    start_urls = [baseurl + tags[count]]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse)

    def parse(self, response):
        tag = self.tags[self.count]
        tagItem = TagItem()
        tagItem['name'] = tag
        # 爬取页面所有表情
        ascii_list = response.xpath("//div[@class='facemoodItemText facemoodItemText-js']/@data-f-text").extract()
        # 过滤没有表情的标签
        if ascii_list:
            tagItem.save()
            for ascii in ascii_list:
                # 存入item
                asciiItem = AsciiEmojiItem()
                asciiItem['tag'] = tagItem
                asciiItem['content'] = ascii

                if isinstance(asciiItem, AsciiEmojiItem):
                    yield asciiItem

        # 爬下一类表情
        self.count += 1
        if self.count < len(self.tags):
            next_url = self.baseurl + self.tags[self.count]
            yield SplashRequest(url=next_url, callback=self.parse)
