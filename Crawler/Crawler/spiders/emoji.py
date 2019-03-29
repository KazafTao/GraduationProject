# -*- coding: utf-8 -*-
import scrapy
from fake_useragent import UserAgent

from Crawler.items import EmojiItem

ua = UserAgent()


# 某个页面（https://www.doutula.com/search?keyword=盘他）查找所有图片网址的xpath语法：
#  //div[@class='random_picture']/a/img/@data-original

class EmojiSpider(scrapy.Spider):
    name = 'emoji'
    # 区别同一类表情包命名的计数器
    count = 1
    # allowed_domains = ['doutula.com']
    keywords = []
    keywords_count = 0
    baseURL = 'https://www.doutula.com/search?keyword='
    # 读取维基百科的流行词列表
    with open("E:/GraduationProject/Crawler/Crawler/datas/words.txt", "r", encoding="utf-8") as hotwords:
        for word in hotwords.readlines():
            keywords.append(word.strip())

    keyword = keywords[keywords_count]
    start_urls = [baseURL + keyword]

    # 设置假UA
    def __init__(self, **kwargs):
        self.headers = {
            'User-Agent': ua.random,
        }

    def parse(self, response):
        # 提取网址的图片连接
        link_list = response.xpath("//div[@class='random_picture']/a/img/@data-original").extract()
        for link in link_list:
            # 存入item
            item = EmojiItem()
            item['id'] = self.count
            self.count += 1
            item['image_link'] = link
            item['type'] = self.keyword
            yield item

        # 找下一个关键词
        self.keywords_count += 1
        if self.keywords_count < len(self.keywords):
            # 重置计数器
            self.count = 1
            self.keyword = self.keywords[self.keywords_count]
            yield scrapy.Request(self.baseURL + self.keyword, callback=self.parse, headers=self.headers)
