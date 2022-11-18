# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Spider1Item(scrapy.Item):
    # define the fields for your item here like:
    id=scrapy.Field()
    question = scrapy.Field()
    # answer = scrapy.Field()
    link=scrapy.Field()
    pass
