import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import ProductItem


class ProductCrawlerSpider(CrawlSpider):
    name = 'product_crawler'
    allowed_domains = ['nike.com']
    start_urls = ['https://www.nike.com/ca/']

    rules = (
        Rule(LinkExtractor(allow=r'https://www.nike.com/ca/w/mens-shoes-nik1zy7ok'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item_links = response.xpath('//a[@class="product-card__link-overlay"]/@href').extract()
        for link in item_links:
            yield scrapy.Request(link, callback=self.parse_detail_page)

    def parse_detail_page(self, response):
        item = ProductItem()
        item['category'] = response.xpath('//h2//text()').extract()
        item['name'] = response.xpath('//h1//text()').extract()
        item['price'] = response.xpath('//*[@class="product-price is--current-price css-1emn094"]//text()').extract()
        item['description'] = response.xpath('//*[@class="description-preview body-2 css-1pbvugb"]//text()').extract()
        item['photo'] = response.xpath('//div[@id="pdp-6-up"]//img/@src').extract()
        yield item
