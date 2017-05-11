import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes_new"
    start_urls = [
                'http://quotes.toscrape.com/page/1/',
                'http://quotes.toscrape.com/page/2/'
                ] 

    def parse(self, response):
        quotes = response.css('div.quote')

        for quote in quotes:
            yield {
                    'text': quote.css('span.text::text').extract_first(),
                    'author': quote.css('small.author::text').extract_first(),
                    'tags': quote.css('div.tags a.tag::text').extract()
                    }

        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback = self.parse)
