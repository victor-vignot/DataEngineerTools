import scrapy


class FranceinfoSpider(scrapy.Spider):
    name = "franceinfo"
    allowed_domains = ["www.franceinfo.fr"]
    start_urls = ["https://www.franceinfo.fr"]

    def parse(self, response):
        pass
