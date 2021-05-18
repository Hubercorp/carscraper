# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class Car(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    model = Field()
    year = Field()
    auction_brand = Field()
    auction_model = Field()
    auction_organizor = Field()
    auction_sales_code = Field()
    auction_restauration_code = Field()
    auction_price = Field()
    auction_location = Field()
    auction_url = Field()
    quote_id = Field()
    
