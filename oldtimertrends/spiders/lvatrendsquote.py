from scrapy import Spider, Request, Field, Item
from scrapy.http import FormRequest
from oldtimertrends.items import Car

class Lvacrawler(Spider):
    name = "lva_quote"
    start_urls = [
        'https://www.lva-auto.fr/cote.php?idMarque=MA55&idModele=-1&rechercheType=1'
    ]

    def parse(self, response):
        auction_url = response.css('.link-result a::attr(href)').get()
        mycar = Car()
        for quote in response.css('ul.cote li'):
            mycar['auction_url'] = auction_url
            mycar['quote_id'] = auction_url.split("=")[1] if mycar['auction_url'] else None
            
    

        next_page = response.css('a.nextItem ::attr(href)').get()

        print(next_page)
        if next_page != "javascript:void()":

            
            yield Request(response.urljoin(next_page), callback=self.parse, dont_filter=True)

        