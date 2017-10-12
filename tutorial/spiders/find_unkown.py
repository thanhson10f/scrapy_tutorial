import scrapy
import json
import csv


class QuotesSpider(scrapy.Spider):
    name = "findproductname"
    custom_settings = {
                'DOWNLOAD_DELAY': 1
            }

    def start_requests(self):
        with open('unknown_product.csv', 'rb') as f:
            code_list = csv.reader(f)

            for code in code_list:
                print(code[0])
                url = 'https://lb1.icheck.com.vn/scan/{}?scan=0'.format(code[0])
                yield scrapy.Request(url=url, callback=self.parse, headers={
                    'icheck-id': 'i-1494218194088',
                    'Authorization': 'Basic aWNoZWNrOmlZQUYmO2NCZSNHM2F+RDojaGVjaw=='
                    })

    def parse_related(self, response):
        json_response = json.loads(response.body_as_unicode())
        data = json_response['data']

        if data and len(data) > 0:
            for item in data:
                code = item['gtin_code']
                item_url = 'https://lb1.icheck.com.vn/scan/{0}?scan=0'.format(code)
                yield scrapy.Request(url=item_url, callback=self.parse, headers={
                    'icheck-id': 'i-1494218194088',
                    'Authorization': 'Basic aWNoZWNrOmlZQUYmO2NCZSNHM2F+RDojaGVjaw=='
                })

    def parse_category(self, response):
        json_response = json.loads(response.body_as_unicode())
        code_list = json_response['data']
        for item in code_list:
            item_url = 'https://lb1.icheck.com.vn/scan/{0}?scan=0'.format(item['gtin_code'])
            yield scrapy.Request(url=item_url, callback=self.parse, headers={
                'icheck-id': 'i-1494218194088',
                'Authorization': 'Basic aWNoZWNrOmlZQUYmO2NCZSNHM2F+RDojaGVjaw=='
            })

    def parse(self, response):
        json_response = json.loads(response.body_as_unicode())
        # print json_response['data']['product_name']
        if 'gtin_code' in json_response['data'] and json_response['data']['product_name']:
            yield json_response['data']
        # code = json_response['data']['gtin_code']
        # yield {
        #        'code': code,
        #        'product_name': json_response['data']['product_name'],
        #        'price_default': json_response['data']['price_default']
        #        }
