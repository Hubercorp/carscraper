
from scrapy import Spider, Request, Field, Item
from scrapy.http import FormRequest
from oldtimertrends.items import Car, Quote

class Lvacrawler(Spider):
    name = "lva_jean"
    start_urls = [
        'https://www.lva-auto.fr/compte/login'
    ]
   
    
    custom_settings = {
        "DUPEFILTER_DEBUG":True,
        "LOG_FILE": "log1258.txt" 
    }

 
    def init (self):
        self.quoteid = None

    
    
   
    def parse (self, response):
        yield FormRequest.from_response(response,
                                        formdata={  "login[username]": "fricadelles@protonmail.com",
	                                                "login[password]": "amLsUYk3WecEhzJ",
	                                                "send": ""},
                                        callback=self.after_login)
    def after_login(self, response):
        yield Request(url = "https://www.lva-auto.fr/cote.php?idMarque=MA230&idModele=-1&rechercheType=1"
            , callback=self.list_quotes, dont_filter= True)
        

    def analyze_auction(self, response):
        
        quote_id = response.request.url.split("idCote=")[1] 
            
        for row in response.css('tr'):
                
            auction_date = row.css('td:nth-child(2)::text').get()
            auction_brand =  row.css('h2::text').get()
            auction_model =  row.css('td:nth-child(3)::text').get()
            auction_organizor =  row.xpath('normalize-space(td[4])').get()
            auction_sales_code =  row.css('td:nth-child(5) abbr::text').get()
            auction_restauration_code =  row.css('td:nth-child(6) abbr::text').get()
            auction_price = row.css('td:nth-child(7)::text').get()
            auction_location = row.css('td:nth-child(8)::text').get()
            
           
            mycar = Car()
            mycar['auction_date'] = auction_date
            mycar['auction_brand'] = auction_brand
            mycar['auction_model'] = auction_model
            mycar['auction_organizor'] = auction_organizor
            mycar['auction_sales_code'] = auction_sales_code
            mycar['auction_restauration_code'] = auction_restauration_code
            mycar['auction_price'] = auction_price
            mycar['auction_location'] = auction_location
            mycar['quote_id'] = quote_id
        # mycar['quote_id'] = self.quoteid
            #print("///////////////",mycar['quote_id'])
            yield mycar


        # next_page = response.css('.nextItem ::attr(href)').get()
        # print(type(next_page))
        
        # if next_page is not None:
        #     print("scrapped from css:",next_page)
            
        #     next_page = response.urljoin('{}&idCote={}'.format(next_page, mycar['quote_id']))
        #     print("reconstructed:",next_page)
            
        #     yield Request(next_page, callback=self.analyze_auction, dont_filter=True)
        #     print("!!!!!!!!!!auction next page yielded!!!!!!!!!!!")

    
    def list_quotes(self, response):
        
        
        brand = response.css('div.textpad a::text').get()
        for quote in response.css('ul.cote li'):

            auction_url = quote.css('.link-result a::attr(href)').get()
            quote_model = quote.css('strong a::text').get(),
            quote_year = quote.css('.pricepad a::text').get(),
            quote_max_price =  quote.css('.cote-max .pricepad::text').get(),
            quote_id = auction_url.split("=")[1] if auction_url else None

            myquote = Quote()

            myquote['auction_url'] = auction_url
            myquote['quote_model'] = quote_model
            myquote['quote_year'] = quote_year
            myquote['quote_max_price'] = quote_max_price
            myquote['quote_id'] = quote_id

            #yield myquote

            
            if auction_url is not None:
                 url = response.urljoin(auction_url)
                
                 yield Request(url, callback=self.analyze_auction, dont_filter=True)
            

                

        next_page = response.css('.nextItem ::attr(href)').get()
        if next_page != "javascript:void()":
                next_page = response.urljoin(next_page)
                yield Request(next_page, callback=self.list_quotes, dont_filter=True)

