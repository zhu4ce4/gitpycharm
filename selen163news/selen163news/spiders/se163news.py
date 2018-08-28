# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request


class Se163newsSpider(scrapy.Spider):
    name = 'se163news'
    # allowed_domains = ['163.com']
    start_urls = ['http://money.163.com/']

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        for sel in response.css('div.ndi_main div.data_row'):
            title = sel.xpath('.//h3/a/text()').extract()
            # title=sel.xpath('string(.//h3/a)').extract_first()
            print(title)
