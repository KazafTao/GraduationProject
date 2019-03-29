# -*- coding: utf-8 -*-
import scrapy
from scrapy_djangoitem import DjangoItem

from Crawler.es_model import ES_Doc
from emoji.models import AsciiEmoji, Tag, EmojiSeries, SeriesElement, Material


class EmojiItem(scrapy.Item):
    id = scrapy.Field()
    image_link = scrapy.Field()
    type = scrapy.Field()
    downloaded = scrapy.Field()
    filetype = scrapy.Field()

    def save_to_es(self):
        doc = ES_Doc()
        doc.type = self['type']
        doc.path = self['type'] + "/" + str(self['id']) + "." + self['filetype']
        doc.downloaded = self['downloaded']
        doc.filetype = self['filetype']
        doc.save()


class AsciiEmojiItem(DjangoItem):
    django_model = AsciiEmoji


class TagItem(DjangoItem):
    django_model = Tag


class EmojiSeriesItem(DjangoItem):
    django_model = EmojiSeries


class SeriesElementItem(DjangoItem):
    django_model = SeriesElement


class MaterialItem(DjangoItem):
    django_model = Material
