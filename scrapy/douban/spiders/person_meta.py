#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 23:41:38 2019

@author: liudiwei
"""

import string
import random
import douban.util as util
import douban.database as db
import douban.validator as validator

from scrapy import Request, Spider
from douban.items import PersonMeta


cursor = db.connection.cursor()

class PersonMetaSpider(Spider):

    name = 'person_item'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
                  (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36'
    allowed_domains = ["Person.douban.com"]

    #select person id from db 
    sql = 'SELECT person_id FROM person_obj WHERE person_id NOT IN (SELECT person_id FROM person) ORDER BY person_id DESC'
    print("select person_id from db: ", sql)
    cursor.execute(sql)
    person_ids = cursor.fetchall()

    start_urls = [
        'https://movie.douban.com/celebrity/%s/' % i['person_id'] for i in person_ids
        # 'https://movie.douban.com/celebrity/1054424/' 
    ]

    def start_requests(self):
        for url in self.start_urls:
            print("======url:", url)
            bid = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(11))
            cookies = {
                'bid': bid,
                'dont_redirect': True,
                'handle_httpstatus_list': [302],
            }

            yield Request(url, cookies=cookies,meta={'main_url':url})

    #获取ID
    def get_person_id(self, meta, response):
        main_url = response.meta['main_url']
        response_url = response.url
        print("##### main_url:", main_url)
        print("##### response_url: ", response_url)

        person_id = main_url.split("celebrity")[1].split("/")[1]
        meta['person_id'] = person_id
        print("==============person_id:", person_id)
        #meta['person_id'] = response.url[33:-1]
        return meta

    #获取性别
    def get_sex(self, meta, response):
        regx = '//div[@class="info"]/ul/li/text()[preceding-sibling::span[text()="性别"]]'
        data = response.xpath(regx).extract()
        print("============get_sex:", data)
        if data:
            meta["sex"] = data[0].strip("\n").split(":")[-1]
        return meta

    #出生日期
    def get_birth(self, meta, response):
        regx = '//div[@class="info"]/ul/li/text()[preceding-sibling::span[text()="出生日期"]]'
        data = response.xpath(regx).extract()
        print("============get_birth:", data)
        if data:
            meta['birth'] = validator.str_to_date(validator.match_date(data[0].strip("\n")))
            if not meta['birth']:
                meta['birth'] = data[0].strip("\n").split(":")[-1]
        return meta


    def get_birthplace(self, meta, response):
        regx = '//div[@class="info"]/ul/li/text()[preceding-sibling::span[text()="出生地"]]'
        data = response.xpath(regx).extract()
        print("============get_birthplace:", data)
        if data:
            meta["birthplace"] = data[0].strip("\n").split(":")[-1]
        return meta

    def get_biography(self, meta, response):
        regx = '//div[@class="article"]/div[@id="intro"]/div[@class="bd"]/span[@class="short"]/text()'
        data = response.xpath(regx).extract()
        if data:
            meta['biography'] = data[0]
        return meta

    def get_profession(self, meta, response):
        regx = '//div[@class="info"]/ul/li/text()[preceding-sibling::span[text()="职业"]]'
        data = response.xpath(regx).extract()
        if data:
            meta['profession'] = data[0].strip("\n").split(":")[-1]
        return meta

    def get_constellatory(self, meta, response):
        regx = '//div[@class="info"]/ul/li/text()[preceding-sibling::span[text()="星座"]]'
        data = response.xpath(regx).extract()
        if data:
            meta['constellatory'] = data[0].strip("\n").split(":")[-1]
        return meta

    def get_name_zh(self, meta, response):
        regx = '//div[@class="info"]/ul/li/text()[preceding-sibling::span[text()="更多中文名"]]'
        data = response.xpath(regx).extract()
        if data:
            meta['name_zh'] = data[0].strip("\n").split(":")[-1]
        return meta

    def get_name_en(self, meta, response):
        regx = '//div[@class="info"]/ul/li/text()[preceding-sibling::span[text()="更多外文名"]]'
        data = response.xpath(regx).extract()
        if data:
            meta['name_en'] = data[0].strip("\n").split(":")[-1]
        return meta

    def parse(self, response):
        print("=====================================+++++++++",response.url)
        if 404 == response.status:
            print("Person.meta.response.url: ",response.url)
        else:
            meta = PersonMeta()
            self.get_person_id(meta, response)
            self.get_sex(meta, response)
            self.get_birth(meta, response)
            self.get_birthplace(meta, response)
            self.get_biography(meta, response)
            self.get_profession(meta, response)
            self.get_constellatory(meta, response)
            self.get_name_zh(meta, response)
            self.get_name_en(meta, response)
            return meta

    def second_parse(self,response):
        """print user-agent"""
        print("\nChange User-Agent: ", response.request.headers['User-Agent'])
