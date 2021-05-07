# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Car(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    model = scrapy.Field()
    year = scrapy.Field()
    auction_brand : scrapy.Field()
    auction_model : scrapy.Field()
    auction_model : scrapy.Field()
    auction_organizor:  scrapy.Field()
    action_sales_code: scrapy.Field()
    auction_restauration_code: scrapy.Field()
    action_price: scrapy.Field()
    action_location: scrapy.Field()
    
