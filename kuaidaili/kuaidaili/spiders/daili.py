# -*- coding: utf-8 -*-
import scrapy
import time
from kuaidaili.items import KuaidailiItem

class DailiSpider(scrapy.Spider):
    header = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'}
    name = "daili"
    allowed_domains = ["kuaidaili.com"]
    start_urls = [
        'http://www.kuaidaili.com/free/outtr/1',
        'http://www.kuaidaili.com/free/intr/1',
        'http://www.kuaidaili.com/free/inha/1',
        'http://www.kuaidaili.com/free/outha/1',
        'http://www.kuaidaili.com/proxylist/1'
    ]

    global COUNT
    COUNT = 0
    def parse(self, response):
        for proxy_server in response.xpath('//tbody//tr'):
            try:
                item = KuaidailiItem()
                item['ip'] = proxy_server.xpath('.//td[@data-title="IP"]/text()').extract()[0].strip()
                item['port'] = proxy_server.xpath('.//td[@data-title="PORT"]/text()').extract()[0].strip()
                yield item
            except:
                pass
        if (response.status == 200) & (len(response.xpath('//tr')) > 5):
            global COUNT
            COUNT += 1
            if COUNT == 10:
                time.sleep(10)
                COUNT = 0
                url = response.url[:len(response.url)-len(response.url.split('/')[-1])]+str(int(response.url.split('/')[-1])+1)
                yield scrapy.Request(url, callback=self.parse)
            else:
                url = response.url[:len(response.url)-len(response.url.split('/')[-1])]+str(int(response.url.split('/')[-1])+1)
                yield scrapy.Request(url, callback=self.parse)
        else:
            print 'Error Page...'

