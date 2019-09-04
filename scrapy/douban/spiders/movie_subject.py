#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 23:41:38 2019

@author: liudiwei
"""

import random
import string
import requests
import json

from douban.items import Subject

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Request, Rule


class MovieSubjectSpider(CrawlSpider):
    name = 'movie_subject'
    allowed_domains = ['m.douban.com', 'movie.douban.com']
    start_urls = ['https://movie.douban.com/cinema/nowplaying/beijing/',
                  'https://movie.douban.com/subject/19899707/']

    """
    start_urls=[]
    #按照分页来
    import douban.database as db
    cursor = db.connection.cursor()
    movie_type = ['剧情', '喜剧', '动作', '爱情', '科幻', '动画', '悬疑', '惊悚', '恐怖', '犯罪', '同性', '音乐', '歌舞', '传记', '历史', '战争', '西部', '奇幻', '冒险', '灾难', '武侠']
    movie_zone = ['中国大陆', '美国', '香港', '台湾', '日本', '韩国', '英国', '法国', '德国', '意大利', '西班牙', '印度', '泰国', '俄罗斯', '伊朗', '加拿大', '澳大利亚', '爱尔兰', '瑞典', '巴西', '丹麦']
    #https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=%E7%94%B5%E5%BD%B1&start=1&genres=剧情&countries=中国大陆
    for type in movie_type:
        for zone in movie_zone:
            if type in ['剧情'] and zone in ['中国大陆', '美国', '香港', '台湾', '日本', '英国', '韩国']:
                continue
            for i in range(0,10000,20):
                print("i is:", i)
                url = str("https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=%E7%94%B5%E5%BD%B1&start={页面}&genres="+ type + "&countries="+ zone +"").format(页面 = i) 
                print(url)
                try:
                    txt = requests.get(url)
                    data = json.loads(txt.text)["data"]
                except:
                    print("over size:")
                    break
                if len(data) == 0:
                    break;
                for each in data:
                    try:
                        print(type, zone, each["url"])
                        douban_id = each["url"].split("subject")[1].split("/")[1]
                        keys = ["douban_id", "type"]
                        values = tuple([douban_id, "movie"])
                        fields = ','.join(keys)
                        temp = ','.join(['%s'] * len(keys))
                        print("start to saved.....")
                        sql = 'INSERT INTO subjects (%s) VALUES (%s)' % (fields, temp)
                        print("data saved.")
                        cursor.execute(sql, values)
                        db.connection.commit()
                    except :
                        print("douban_id duplicated.")
    """

    rules = (
        Rule(LinkExtractor(allow=('movie.douban.com/subject/(\d).*/')),
             callback='parse_item', follow=True, process_request='cookie'),

        Rule(LinkExtractor(allow=('movie/subject/(\d).*rec$')),
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
        print("\n\nresponse.url:", response.url)

        subject['douban_id'] = response.url.split("subject")[1].split("/")[1]
        #subject['douban_id'] = response.url[35:-10]
        return subject

    def parse_item(self, response):
        print("===================parse_item")
        subject = Subject()
        self.get_douban_id(subject, response)
        subject['type'] = 'movie'
        print("\nChange User-Agent: ", response.request.headers['User-Agent'])
        return subject
