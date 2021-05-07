
from scrapy import Spider, Request, Field, Item
from scrapy.http import FormRequest
from oldtimertrends.items import Car

class Lvacrawler(Spider):
    
    code = ("MA55","MA124","MA236")
    name = "lva_jean"
    start_urls = (
        'https://www.lva-auto.fr/compte/login',
    )
    def __init__(self):
        self.model = None
        self.year = None
        self.current_url = None
 
    def parse (self, response):
        yield FormRequest.from_response(response,
                                        formdata={  "login[username]": "fricadelles@protonmail.com",
	                                                "login[password]": "amLsUYk3WecEhzJ",
	                                                "send": ""},
                                        callback=self.after_login)
    def after_login(self, response):
            yield Request(url = "https://www.lva-auto.fr/cote.php?idMarque=MA236&idModele=-1&rechercheType=1"
            , callback=self.list_quotes)
    def analyze_auction(self, response):
        
        quote_id = response.request.url.split("=")[1]
        #print(self.model, "!!!!!!!!!!model at AUCTION LEVEL!!!!!!!")
        for row in response.css('tr'):
                
            print(self.model, "\\\\\\\\")
            auction_brand =  row.css('h2::text').get()
            auction_model =  row.css('td:nth-child(3)::text').get()
            auction_organizor =  row.xpath('normalize-space(td[4])').get()
            auction_sales_code =  row.css('td:nth-child(5) abbr::text').get()
            auction_restauration_code =  row.css('td:nth-child(6) abbr::text').get()
            auction_price = row.css('td:nth-child(7)::text').get()
            auction_location = row.css('td:nth-child(8)::text').get()

            mycar= Car()
            mycar['model'] = self.model
            mycar['year'] = self.year
            mycar['auction_brand'] = auction_brand
            mycar['auction_model'] = auction_model
            mycar['auction_organizor'] = auction_organizor
            mycar['auction_sales_code'] = auction_sales_code
            mycar['auction_restauration_code'] = auction_restauration_code
            mycar['auction_price'] = auction_price
            mycar['auction_location'] = auction_location
            mycar['quote_id'] = quote_id
            yield mycar


                
        next_page = response.css('.nextItem ::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin("{}&idCote={}".format(next_page, quote_id))
            yield Request(next_page, callback=self.analyze_auction)
        else: 
            yield Request(self.current_url, callback=self.list_quotes)
    
    def list_quotes(self, response):
        auction_url = None
        mycar= Car()
        
        for quote in response.css('ul.cote li'):
            self.model = quote.css('strong a::text').get()
            self.year = quote.css('.pricepad a::text').get() 
            auction_url = quote.css('.link-result a::attr(href)').get()
            self.current_url = response.request.url
            print(self.current_url,'-------URL------')
            if auction_url != None:
                 url = response.urljoin(auction_url)
                
                 yield Request(url, callback=self.analyze_auction)
            
            # else:
            #      mycar= Car()
            #      mycar['model'] = self.model
            #      mycar['year'] = self.year
            #      print('without a',mycar)
            #      yield mycar

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