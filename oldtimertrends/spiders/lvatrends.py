
from scrapy import Spider, Request, Field, Item
from scrapy.http import FormRequest
#from oldtimertrends.items import Car
from ..items import Car
class Lvacrawler(Spider):
    mycar = Car()
    code = ("MA55","MA124")
    name = "lva_jean"
    start_urls = (
        'https://www.lva-auto.fr/compte/login',
    )

 
    def parse (self, response):
        yield FormRequest.from_response(response,
                                        formdata={  "login[username]": "fricadelles@protonmail.com",
	                                                "login[password]": "amLsUYk3WecEhzJ",
	                                                "send": ""},
                                        callback=self.after_login)
    def after_login(self, response):
            yield Request(url = "https://www.lva-auto.fr/cote.php?idMarque=MA55&idModele=-1&rechercheType=1"
            , callback=self.list_quotes)
    def analyze_auction(self, response):
        quote_id = response.request.url.split("=")[1]
        for row in response.css('tr'):
                yield {
                    'auction_brand' : row.css('h2::text').get(),
                    'auction_model' : row.css('td:nth-child(3)::text').get(),
                    'auction_organizor':  row.xpath('normalize-space(td[4])').get(),
                    'action_sales_code' : row.css('td:nth-child(5) abbr::text').get(),
                    'auction_restauration_code' : row.css('td:nth-child(6) abbr::text').get(),
                    'action_price': row.css('td:nth-child(7)::text').get(),
                    'action_location': row.css('td:nth-child(8)::text').get(),
                }
        next_page = response.css('.nextItem ::attr(href)').get()
        if next_page:
            next_page = response.urljoin("{}&idCote={}".format(next_page, quote_id))
            yield Request(next_page, callback=self.analyze_auction)
    
    def list_quotes(self, response):
        for quote in response.css('ul.cote li'):
           
            auction_url = quote.css('.link-result a::attr(href)').get()
                
                # model = quote.css('strong a::text').get()
                # year = quote.css('.pricepad a::text').get()
                # 'max_price': quote.css('.cote-max .pricepad::text').get(),
                 #'auction_url': auction_url, 
                # 'auctions': [],
                # 'quote_id': quote_id
            if auction_url:
                url = response.urljoin(auction_url)
                yield Request(url, callback=self.analyze_auction)
            
            next_page = response.css('.nextItem ::attr(href)').get()
            if next_page != "javascript:void()":
                next_page = response.urljoin(next_page)
                yield Request(next_page, callback=self.list_quotes)

""" class OldtimertrendsItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    auction_brand : Field()
    auction_model : Field()
    auction_model : Field()
    auction_organizor: Field()
    action_sales_code: Field()
    auction_restauration_code: Field()
    action_price: Field()
    action_location: Field() """