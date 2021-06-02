
from scrapy import Spider, Request, Field, Item
from scrapy.http import FormRequest
from oldtimertrends.items import Car

class Lvacrawler(Spider):
    
    name = "lva_jeanne"
    start_urls = [
        'https://www.lva-auto.fr/compte/login'
    ]
    MODELS = [4175]
   
    def parse (self, response):
        yield FormRequest.from_response(response,
                                        formdata={  "login[username]": "fricadelles@protonmail.com",
	                                                "login[password]": "amLsUYk3WecEhzJ",
	                                                "send": ""},
                                        callback=self.after_login)
    def after_login(self, response):
        for model in range(len(self.MODELS)):   
            yield Request(url = "https://www.lva-auto.fr/cote.encheres.php?idCote={}".format(self.MODELS[model])
            , callback=self.analyze_auction)

        
    def analyze_auction(self, response):
        
        quote_id = response.request.url.split("=")[1]
        for row in response.css('tr'):
                
            auction_date = row.css('td:nth-child(2)::text').get()
            auction_brand =  row.css('h2::text').get()
            auction_model =  row.css('td:nth-child(3)::text').get()
            auction_organizor =  row.xpath('normalize-space(td[4])').get()
            auction_sales_code =  row.css('td:nth-child(5) abbr::text').get()
            auction_restauration_code =  row.css('td:nth-child(6) abbr::text').get()
            auction_price = row.css('td:nth-child(7)::text').get()
            auction_location = row.css('td:nth-child(8)::text').get()

            mycar= Car()
            mycar['auction_date'] = auction_date
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
        if next_page:
            print("FROM",next_page)
            next_page = response.urljoin(next_page)
            print("TO",next_page)
            yield Request(next_page, callback=self.analyze_auction)

