
from scrapy import Spider, Request, Field, Item
from scrapy.http import FormRequest
from oldtimertrends.items import Car

class Lvacrawler(Spider):
    name = "lva_jean"
    start_urls = [
        'https://www.lva-auto.fr/compte/login'
    ]
   
    
    
    def init (self):
        self.quoteid = None

    
    
   
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
        print('/////////////', quote_id)
            # self.quoteid = quote_id
        
        
        for row in response.css('tr'):
                

            auction_brand =  row.css('h2::text').get()
            auction_model =  row.css('td:nth-child(3)::text').get()
            auction_organizor =  row.xpath('normalize-space(td[4])').get()
            auction_sales_code =  row.css('td:nth-child(5) abbr::text').get()
            auction_restauration_code =  row.css('td:nth-child(6) abbr::text').get()
            auction_price = row.css('td:nth-child(7)::text').get()
            auction_location = row.css('td:nth-child(8)::text').get()
            
           
            mycar = Car()
            mycar['auction_brand'] = auction_brand
            mycar['auction_model'] = auction_model
            mycar['auction_organizor'] = auction_organizor
            mycar['auction_sales_code'] = auction_sales_code
            mycar['auction_restauration_code'] = auction_restauration_code
            mycar['auction_price'] = auction_price
            mycar['auction_location'] = auction_location
            mycar['quote_id'] = quote_id
        # mycar['quote_id'] = self.quoteid
            print("///////////////",mycar['quote_id'])
            yield mycar


        next_page = response.css('.nextItem ::attr(href)').get()
        
        if next_page is not None:
            print("from///////////////////////////////",next_page)
            next_page = response.urljoin(next_page)
            url_for_next_page_1 = 'idCote={}&{}'.format(mycar['quote_id'], next_page)
            url_for_next_page_2 = '{}&idCote={}'.format(next_page, mycar['quote_id'])
            next_page = response.urljoin(url_for_next_page_2)
            print("to///////////////////////////////",next_page)
            yield Request(next_page, callback=self.list_quotes)
    
    def list_quotes(self, response):
        
        
        for quote in response.css('ul.cote li'):
            auction_url = quote.css('.link-result a::attr(href)').get()
            # quote_id = auction_url.split("=")[1] if auction_url else None
            # self.quoteid = quote_id
            # print("//////////////",self.quoteid)

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