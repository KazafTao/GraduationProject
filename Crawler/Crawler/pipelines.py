# -*- coding: utf-8 -*-
import os

import requests
from scrapy.pipelines.images import ImagesPipeline

from Crawler.settings import IMAGES_STORE as images_store
from emoji.models import EmojiSeries, Tag
from items import SeriesElementItem, EmojiSeriesItem


def save_form_url(file_path, url):
    with open(file_path, 'wb') as handle:
        response = requests.get(url, stream=True)
        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)


class DownloadEmojiPipeline(ImagesPipeline):
    def process_item(self, item, spider):
        dir_path = '%s/%s/%s' % (images_store, spider.name, item['type'])
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        image_link = item['image_link']
        item['filetype'] = image_link[-3:]
        file = str(item['id']) + "." + item['filetype']
        file_path = '%s/%s' % (dir_path, file)

        # 将图片写入文件
        with open(file_path, 'wb') as handle:
            response = requests.get(image_link, stream=True)
            if (response.status_code == 200):
                item['downloaded'] = True
            else:
                item['downloaded'] = False
            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)

        return item


class EsPipeline(object):
    def process_item(self, item, spider):
        if item['downloaded']:
            item.save_to_es()
        return item


class DownloadEmojiSetPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, EmojiSeriesItem):
            dir_path = '%s/%s/%s' % (images_store, spider.name, item['name'])
            item['path'] = dir_path
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            item.save()
            return item

        if isinstance(item, SeriesElementItem):
            # 获取该表情的系列
            series = EmojiSeries.objects.get(name=item['series']['name'])
            # 获取该表情的路径
            count = series.num
            filetype = item['url'][-3:]
            if filetype == 'peg':
                filetype = 'jpeg'
            file = str(count) + "." + filetype
            item['path'] = '%s/%s' % (series.name, file)
            file_path = '%s/%s' % (series.path, file)
            series.num += 1
            series.save()

            # 将图片写入文件
            save_form_url(file_path,item['url'])

            # 保存外键
            item['series'] = EmojiSeries.objects.get(name=item['series']['name'])
            item.save()
            return item


class AsciiPipeline(object):
    def process_item(self, item, spider):
        # 存入Django Models
        item['tag'] = Tag.objects.get(name=item['tag']['name'])
        item.save()
        return item


class DownloadMaterialPipeline(ImagesPipeline):
    def process_item(self, item, spider):
        dir_path = '%s/%s' % (images_store, spider.name)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        url = item['url']
        item['filetype'] = url[-3:]
        if item['filetype'] == 'peg':
            item['filetype'] = 'jpeg'
        file = str(item['name']) + "." + item['filetype']
        file_path = '%s/%s' % (dir_path, file)
        item['path'] = file

        # 将图片写入文件
        save_form_url(file_path, url)
        item.save()

        return item
