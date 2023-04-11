import scrapy
from scrapy import Request


class GetbooksSpider(scrapy.Spider):
    name = 'getbooks'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        for x in response.xpath('//article[@class="product_pod"]'):
            title = x.xpath('//h3/a/@title').extract_first()
            
            price = x.xpath('//div[@class="product_price"]/p[@class="price_color"]/text()').extract_first()
            
            star = x.xpath('//p/@class').extract_first().split()[-1]
            
            rel_url = x.xpath('//h3/a/@href').extract_first()
            abs_url = response.urljoin(rel_url)
            
            yield Request(abs_url, callback = self.parse_page, dont_filter = True, meta = {'Title': title, 'Price': price, 'Star': star, 'URL': abs_url})
        
        rel_next_url = response.xpath('//li[@class="next"]/a/@href').extract_first()
        abs_next_url = response.urljoin(rel_next_url)
        
        yield Request(abs_next_url, callback = self.parse)

    def parse_page(self, response):
        title = response.meta['Title']
        price = response.meta['Price']
        star = response.meta['Star']
        abs_url = response.meta['URL']
        avail = response.xpath('//p[@class="instock availability"]/text()').extract()
        desc = response.xpath('//div[@id="product_description"]/following-sibling::p/text()').extract_first().strip()
        
        yield {'Title': title, 'Price': price, 'Star': star, 'URL': abs_url, 'Availability': avail, 'Description': desc}
       
        