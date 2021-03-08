# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GbParseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class GbAutoYoulaItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    list_img = scrapy.Field()
    parameters = scrapy.Field()
    description = scrapy.Field()
    user_url = scrapy.Field()

class GbHhItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    salary = scrapy.Field()
    description1 = scrapy.Field()
    description2 = scrapy.Field()
    skills = scrapy.Field()
    url_company = scrapy.Field()
    
    