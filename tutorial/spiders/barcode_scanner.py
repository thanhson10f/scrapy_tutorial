import scrapy
import json

class QuotesSpider(scrapy.Spider):
    name = "barcode"
    custom_settings = {
                'DOWNLOAD_DELAY': 1
            }
    def start_requests(self):
        urls = [
                'https://mining.icheck.com.vn/popular/category?parent_category_id=13&limit=500'
                ] 
        for url in urls:
            yield scrapy.Request(url = url, callback = self.parse_category, headers = {
                'icheck-id':'i-1494218194088',
                'Authorization':'Basic aWNoZWNrOmlZQUYmO2NCZSNHM2F+RDojaGVjaw=='
                })
    def parse_related(self, response):
        json_response = json.loads(response.body_as_unicode())
        data = json_response['data']

        if data and len(data)>0:
            for item in data:
                code = item['gtin_code']
                item_url = 'https://lb1.icheck.com.vn/scan/{0}?scan=0'.format(code)
                yield scrapy.Request(url = item_url, callback = self.parse, headers = {
                    'icheck-id':'i-1494218194088',
                    'Authorization':'Basic aWNoZWNrOmlZQUYmO2NCZSNHM2F+RDojaGVjaw=='
                })
    def parse_category(self, response):
        json_response = json.loads(response.body_as_unicode())
        code_list = json_response['data']
        for item in code_list:
            item_url = 'https://lb1.icheck.com.vn/scan/{0}?scan=0'.format(item['gtin_code'])
            yield scrapy.Request(url = item_url, callback = self.parse, headers = {
                'icheck-id':'i-1494218194088',
                'Authorization':'Basic aWNoZWNrOmlZQUYmO2NCZSNHM2F+RDojaGVjaw=='
            })
           
    def parse(self, response):
        json_response = json.loads(response.body_as_unicode())
        #print json_response['data']['product_name']
        code = json_response['data']['gtin_code']
        #yield {
        #        'code': code,
        #        'product_name': json_response['data']['product_name'],
        #        'price_default': json_response['data']['price_default']
        #        }
        yield json_response['data'] 
        related_url = 'https://mining.icheck.com.vn/scan/related/{0}'.format(code)
        
        yield scrapy.Request(url = related_url, callback = self.parse_related, headers = {
                'icheck-id':'i-1494218194088',
                'Authorization':'Basic aWNoZWNrOmlZQUYmO2NCZSNHM2F+RDojaGVjaw=='
                })
#        next_page = response.css('li.next a::attr(href)').extract_first()
#        if next_page is not None:
#            next_page = response.urljoin(next_page)
#            yield scrapy.Request(next_page, callback = self.parse)
            
