import scrapy
import json
import re


class QuotesSpider(scrapy.Spider):
    name = "gmatdup"
    custom_settings = {
                'DOWNLOAD_DELAY': 1
            }

    def start_requests(self):
        urls = [
            'http://gmat.kmf.com/question/rc/gwd'
                ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_category)

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
        question_links = response.css('table.subject-table tbody tr')
        for link in question_links:
            url = link.xpath('td[2]/a/@href').extract_first().strip()
            number = link.xpath('td[1]/text()').extract_first().strip()
            # print(number + " - " + url)
            yield scrapy.Request(url=url, callback=self.parse, meta={'number': number})

        next_url = response.css('a.next').xpath('@href').extract_first()
        if '?page=' in next_url:
            n_url = response.urljoin(next_url)
            yield scrapy.Request(url=n_url, callback=self.parse_category)

        # json_response = json.loads(response.body_as_unicode())
        # code_list = json_response['data']
        # for item in code_list:
        #     item_url = 'https://lb1.icheck.com.vn/scan/{0}?scan=0'.format(item['gtin_code'])
        #     yield scrapy.Request(url=item_url, callback=self.parse, headers={
        #         'icheck-id': 'i-1494218194088',
        #         'Authorization': 'Basic aWNoZWNrOmlZQUYmO2NCZSNHM2F+RDojaGVjaw=='
        #     })

    def parse(self, response):
        content = response.css('div.sub-content')
        enid = content.css('div.right-options li.active').xpath('@enid').extract_first()
        qid_link = content.css('div.right-options li.active a').xpath('@href').extract_first()
        match = re.search(r'(\w+)-(\d+)', qid_link)
        qid = ''
        subid = 0
        if match:
            qid = match.group(1)
            subid = int(match.group(2))
        text = ''.join(content.css('div.left-text').xpath('node()').extract()).strip()
        options = content.css('ul.options li')
        # options = re.sub(r'<a[^>]+>[^>]+>', '', options)
        answer = content.css('div.show-answer span::text').extract_first()
        option_list = []
        for opt in options:
            choice = opt.xpath('span/text()').extract_first()
            body = opt.css('::text').extract()[1].strip()
            # print("*"*10)
            # print(body)
            # body = re.sub('<[^>]*>', '', body)
            option_list.append([choice, body])

        number = response.meta['number']
        yield {
            'number': int(number),
            'text': text,
            'enid': enid,
            'qid': qid,
            'subid': subid,
            'options': option_list,
            'answer': answer
        }
        # with open('gmat.html', 'a') as f:
        #     txt = "<div class='question'>"+response.meta['number']+". "+text+options+'</div>\n'
        #     f.write(txt)
        # json_response = json.loads(response.body_as_unicode())
        # code = json_response['data']['gtin_code']
        # yield {
        #        'code': code,
        #        'product_name': json_response['data']['product_name'],
        #        'price_default': json_response['data']['price_default']
        #        }
        # yield json_response['data']
        # related_url = 'https://mining.icheck.com.vn/scan/related/{0}'.format(code)
        # yield scrapy.Request(url=related_url, callback=self.parse_related, headers={
        #         'icheck-id': 'i-1494218194088',
        #         'Authorization': 'Basic aWNoZWNrOmlZQUYmO2NCZSNHM2F+RDojaGVjaw=='
        #         })
#        next_page = response.css('li.next a::attr(href)').extract_first()
#        if next_page is not None:
#            next_page = response.urljoin(next_page)
#            yield scrapy.Request(next_page, callback = self.parse)
