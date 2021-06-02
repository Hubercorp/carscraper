from scrapy import Spider, Request, Field, Item
from scrapy.http import FormRequest
from oldtimertrends.items import Car
from scrapy.utils.response import open_in_browser
class Lvacrawler(Spider):
    name = "lva_scrapeuse"
    start_urls = [
        'https://www.lva-auto.fr/compte/login'
    ]
   
    
    custom_settings = {
        "DUPEFILTER_DEBUG":True,
        "LOG_FILE": "log0744.txt" 
    }


    
    def connect_to_login(self, response):
        yield Request(url = 'https://www.lva-auto.fr/compte/login', callback=self.parse )
   
    def parse (self, response):
        yield FormRequest.from_response(response,
                                        formdata={  "login[username]": "spidercochonx@protonmail.com",
	                                                "login[password]": "MQ2kATcqtV!h6xJ",
	                                                "send": ""},
                                        callback=self.after_login)
    def after_login(self, response):
        
        yield Request(url = "https://www.lva-auto.fr/cote.encheres.php?idCote=6932"
            , callback=self.list_quotes, dont_filter= True)
        

    def analyze_auction(self, response):
        open_in_browser(response)
         
            
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

        
            yield mycar


        # next_page = response.css('.nextItem ::attr(href)').get()
        # print(next_page)
        
        # if next_page is not None:
        #     print("scrapped from css:",next_page)
            
        #     next_page = response.urljoin('{}&idCote={}'.format(next_page, mycar['quote_id']))
        #     print("reconstructed:",next_page)
            
        #     yield Request(next_page, callback=self.analyze_auction, dont_filter=True)
        #     print("!!!!!!!!!!auction next page yielded!!!!!!!!!!!")

    
    def list_quotes(self, response):
        open_in_browser(response)
        
        for quote in response.css('ul.cote li'):
            auction_url = quote.css('.link-result a::attr(href)').get()
            quote_id = auction_url.split("=")[1] if auction_url else None
            self.quoteid = quote_id
            print("//////////////",self.quoteid)

            if auction_url is not None:
                url = response.urljoin(auction_url)
                yield Request(url, callback=self.analyze_auction)
            

                

        next_page = response.css('a.nextItem ::attr(href)').get()
        page_number = next_page.split("page=")[1]
        print("PAAAAGE NUUUUMBEEEER", page_number)
        print(next_page)
        base_url = "https://www.lva-auto.fr/cote.php?cote_php?"
        if next_page != "javascript:void()":
                next_page2 = base_url + str(next_page)
                print(next_page2)
                yield Request(next_page2, callback=self.list_quotes, dont_filter=True)


