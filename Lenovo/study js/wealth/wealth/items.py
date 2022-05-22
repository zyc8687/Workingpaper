# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WealthItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    code = scrapy.Field()
    price_limit = scrapy.Field()
    trading_turnover = scrapy.Field()
    trading_volume = scrapy.Field()
    ampl = scrapy.Field()
    max_price = scrapy.Field()
    mini_price = scrapy.Field()
    yesterday_price = scrapy.Field()
    quantity_ratio = scrapy.Field()
    turnover_rate = scrapy.Field()
    PE = scrapy.Field()
    PB = scrapy.Field()
    plate = scrapy.Field()
    list_key = scrapy.Field()

