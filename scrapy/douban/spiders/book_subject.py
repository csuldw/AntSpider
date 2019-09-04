#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 23:41:38 2019

@author: liudiwei
"""

import random
import string

from douban.items import Subject

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Request, Rule


class BookSubjectSpider(CrawlSpider):
    name = 'book_subject'
    allowed_domains = ['m.douban.com',"book.douban.com"]
    start_urls = ['https://book.douban.com/subject/25862578/']
    #rules = (
    #    Rule(LinkExtractor(allow=('book/subject/(\d).*rec$')),
    #         callback='parse_item', follow=True, process_request='cookie'),
    #)

    rules = (
        Rule(LinkExtractor(allow=('book.douban.com/subject/(\d).*/')),
             callback='parse_item', follow=True, process_request='cookie'),

        Rule(LinkExtractor(allow=('book/subject/(\d).*rec$')),
             callback='parse_item', follow=True, process_request='cookie'),
    )

    def cookie(self, request):
        bid = ''.join(random.choice(string.ascii_letters + string.digits) for
                      x in range(11))
        request.cookies['bid'] = bid
        request = request.replace(url=request.url.replace('?', '/?'))
        return request

    def start_requests(self):
        for url in self.start_urls:
            bid = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(11))
            yield Request(url, cookies={'bid': bid})

    def get_douban_id(self, subject, response):
        subject['douban_id'] = response.url[34:-10]
        return subject

    def parse_item(self, response):
        subject = Subject()
        self.get_douban_id(subject, response)
        subject['type'] = 'book'
        print("\nChange User-Agent: ", response.request.headers['User-Agent'])
        return subject
