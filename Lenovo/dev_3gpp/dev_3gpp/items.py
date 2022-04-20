# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Dev3GppItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    meeting = scrapy.Field()
    time = scrapy.Field()
    c_name = scrapy.Field()
    r_name = scrapy.Field()
    c_company = scrapy.Field()
    r_company = scrapy.Field()
    pass
