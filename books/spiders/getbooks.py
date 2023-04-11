import scrapy
from scrapy import Request

class GetbooksSpider(scrapy.Spider):
    name = 'getbooks'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        for book in response.xpath('//article[@class="product_pod"]'):
            rel_url = book.xpath('.//h3/a/@href').get()
            abs_url = response.urljoin(rel_url)
            
            yield Request(abs_url, callback=self.parse_book, meta={'url': abs_url})

        next_url = response.xpath('//li[@class="next"]/a/@href').get()
        if next_url:
            yield response.follow(next_url, callback=self.parse)

    def parse_book(self, response):
        url = response.meta['url']
        title = response.xpath('//h1/text()').get().strip()
        price = response.xpath('//p[@class="price_color"]/text()').get()
        rating = response.xpath('//p[contains(@class, "star-rating")]/@class')
        star = rating.get().split()[-1] if rating else None
        desc = response.xpath('//div[@id="product_description"]/following-sibling::p/text()')
        desc = desc.get().strip() if desc else 'No description available'

        yield {'url': url, 'Title': title, 'Price': price, 'Star': star, 'Description': desc}
