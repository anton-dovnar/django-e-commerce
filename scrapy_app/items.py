# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductItem(scrapy.Item):
    category = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    size = scrapy.Field
    photo = scrapy.Field()
