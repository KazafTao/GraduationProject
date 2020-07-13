import scrapy
import datetime
from items import MaterialItem


class MaterialSpider(scrapy.Spider):
    name = 'material'
    # allowed_domains = ['fabiaoqing.com']
    prefix = "https://fabiaoqing.com/"
    baseurl = "https://fabiaoqing.com/diy/lists/page/"
    page = 1
    start_urls = [baseurl + str(page) + ".html"]
    start_time=datetime.datetime.now()


    def get_name_from_title(self, title):
        pos = title.find("表情包制作")
        title = title[:pos].strip()
        if title.endswith('_') or title.endswith('-'):
            name = title[:-1]
            return name
        else:
            name = str
            return name

    @staticmethod
    def close(spider, reason):
        closed = getattr(spider, 'closed', None)
        if callable(closed):
            endtime=datetime.datetime.now()
            print("共花费%d秒",(spider.start_time-endtime).seconds)
            return closed(reason)

    def parse(self, response):
        node_list = response.xpath("//div[@class='ui card']")
        for node in node_list:
            item = MaterialItem()
            title = node.xpath('.//a/@title').extract()[0]
            item['name'] = self.get_name_from_title(title)
            item['url'] = node.xpath('.//img/@data-original').extract()[0]
            yield item

        if self.page < 39:
            self.page = self.page + 1
            yield scrapy.Request(self.baseurl + str(self.page) + ".html", callback=self.parse)
