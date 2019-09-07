#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 23:41:38 2019

@author: liudiwei
"""

import json
import random
import string

import douban.database as db
from douban.items import Comment
from lxml import etree
from scrapy import Request, Spider

cursor = db.connection.cursor()

#爬取热门评论：最多啊220条
class MovieCommentSpider(Spider):
    name = 'movie_comment'
    allowed_domains = ['movie.douban.com']
    # sql = "SELECT douban_id FROM movies where douban_id not in (\
    #     select douban_id from (select douban_id,count(*) num from comments GROUP BY douban_id) a where a.num>1\
    # )"
    ##修改查询语句
    sql = "SELECT douban_id FROM movies where douban_id not in (\
        select douban_id from (select douban_id,count(*) num from comments GROUP BY douban_id) a where a.num > 20\
    )"
    cursor.execute(sql)
    movies = cursor.fetchall()
    random.shuffle(movies)
    start_urls = {
        str(i['douban_id']): ('https://movie.douban.com/subject/%s/comments?status=P' % i['douban_id']) for i in movies
        #str(i['douban_id']): ('https://movie.douban.com/subject/%s/comments?sort=time&status=P' % i['douban_id']) for i in movies

        #https://movie.douban.com/subject/26709258/comments?sort=time&status=P
    }


    def start_requests(self):
        for (key, url) in self.start_urls.items():
            # headers = {
            #     'Referer': 'https://m.douban.com/movie/subject/%s/comments' % key
            # }
            bid = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(11))
            cookies = {
                'bid': bid,
                'dont_redirect': True,
                'handle_httpstatus_list': [302],
            }
            yield Request(url, cookies=cookies,meta={'main_url':url})

    def parse(self, response):
        main_url = response.meta['main_url']
        response_url = response.url
        #print("##### main_url:", main_url)
        #print("##### response_url: ", response_url)
        # regx = '//a[preceding-sibling::span[text()="< 前页"]][following-sibling::div]/@href'
        #regx = '//span[@class="prev"]/text()'
        
        if 404 == response.status:
            print("movie.meta.response.url: ",response.url)
        else:
            douban_id = main_url.split("subject")[1].split("/")[1]

            #下一页
            regx = '//a[@class="next"]/@href'
            next_url = response.xpath(regx).extract()

            #先获取item
            item_regx = '//div[@class="comment-item"]'
            comment_item_list = response.xpath(item_regx).extract()

            #print("comment_item_list======:",comment_item_list)
            if len(comment_item_list) > 1:
                for resp_item in comment_item_list:
                    # print("==============douban_id:", douban_id)
                    print("resp_item======:",resp_item)
                    resp_item = etree.HTML(resp_item)
                    #用户url
                    url_regx = '//div[@class="avatar"]/a/@href'        
                    url_list = resp_item.xpath(url_regx)
                    print("\n+++++++++++++++++++++++++url_list",url_list)

                    #用户
                    username_regx = '//div[@class="avatar"]/a/@title'        
                    username_list = resp_item.xpath(username_regx)
                    # print("\n+++++++++++++++++++++++++",username_list)

                    #头像路径
                    avator_regx = '//div[@class="avatar"]/a/img/@src'        
                    avator_list = resp_item.xpath(avator_regx)
                    #print("\n+++++++++++++++++++++++++",avator_list)
                    
                    #投票数量
                    vote_regx = '//div[@class="comment"]/h3/span/span[@class="votes"]/text()'        
                    vote_list = resp_item.xpath(vote_regx)
                    print("\n+++++++++++++++++++++++++vote_list:",vote_list)

                    #评分
                    rating_regx = '//div[@class="comment"]/h3/span[@class="comment-info"]/span[contains(@class,"allstar")]/@class'        
                    rating_list = resp_item.xpath(rating_regx)
                    print("\n+++++++++++++++++++++++++rating", rating_list)

                    #评论时间
                    comment_time_regx = '//div[@class="comment"]/h3/span[@class="comment-info"]/span[contains(@class,"comment-time")]/@title'        
                    comment_time_list = resp_item.xpath(comment_time_regx)
                    print("\n+++++++++++++++++++++++++comment_time", comment_time_list)

                    # 内容
                    comment_regx = '//div[@class="comment"]/p/span[@class="short"]/text()'        
                    comment_list = resp_item.xpath(comment_regx)
                    # print("\n+++++++++++++++++++++++++",comment_list)

                    #评论ID
                    comment_id_regx = '//div[@class="comment"]/h3/span/input/@value'        
                    comment_id_list = resp_item.xpath(comment_id_regx)
                    # print("\n+++++++++++++++++++++++++",comment_id_list)

                    # for i in range(len(comment_list)):
                    comment = Comment()
                    comment['douban_id'] = douban_id
                    comment['douban_comment_id'] = comment_id_list[0] if len(comment_id_list) > 0 else ""
                    comment['douban_user_nickname'] = username_list[0] if len(username_list) > 0 else ""
                    comment['douban_user_avatar'] = avator_list[0] if len(avator_list) > 0 else ""
                    comment['douban_user_url'] = url_list[0] if len(url_list) > 0 else ""
                    comment['content'] = comment_list[0] if len(comment_list) > 0 else ""
                    comment['votes'] = vote_list[0] if len(vote_list) > 0 else ""
                    comment['rating'] = rating_list[0] if len(rating_list) > 0 else ""
                    comment['comment_time'] = comment_time_list[0] if len(comment_time_list) > 0 else ""
                    yield comment

            
            if len(next_url)>0:
                url = "https://movie.douban.com/subject/%s/comments%s" %(douban_id, next_url[0])
                print("=====request Next url================:", url)
                bid = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(11))
                cookies = {
                    'bid': bid,
                    'dont_redirect': True,
                    'handle_httpstatus_list': [302],
                }
                yield Request(url, cookies=cookies,meta={'main_url':url})

    def second_parse(self,response):
        """print user-agent"""
        print("\nChange User-Agent: ", response.request.headers['User-Agent'])

