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
from douban.items import MovieMeta


cursor = db.connection.cursor()


class MovieMetaSpider(Spider):

    name = 'movie_meta'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
                  (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36'
    allowed_domains = ["movie.douban.com"]
    #select subject id from db where type eq movie and id not obtain
    sql = 'SELECT * FROM subjects WHERE type="movie" AND douban_id NOT IN (SELECT douban_id FROM movies) ORDER BY douban_id DESC'
    print("select movies from db: ", sql)
    cursor.execute(sql)
    movies = cursor.fetchall()
    douban_list = [ i['douban_id'] for i in movies]
    start_urls = (
        'https://movie.douban.com/subject/%s/' % i['douban_id'] for i in movies
    )

    #print("+++++douban_list", douban_list)

    def start_requests(self):
        for url in self.start_urls:
            bid = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(11))
            cookies = {
                'bid': bid,
                'dont_redirect': True,
                'handle_httpstatus_list': [302],
            }
            yield Request(url, cookies=cookies,meta={'main_url':url})

    def get_douban_id(self, meta, response):
        main_url = response.meta['main_url']
        response_url = response.url
        print("##### main_url:", main_url)
        print("##### response_url: ", response_url)

        douban_id = main_url.split("subject")[1].split("/")[1]
        meta['douban_id'] = douban_id
        print("==============douban_id:", douban_id)
        #meta['douban_id'] = response.url[33:-1]
        return meta

    def get_type(self, meta, response):
        regx = '//text()[preceding-sibling::span[text()="集数:"]][fo\
llowing-sibling::br]'
        data = response.xpath(regx).extract()
        if data:
            meta['type'] = 'tv'
        else:
            meta['type'] = 'movie'
        return meta

    def get_cover(self, meta, response):
        regx = '//img[@rel="v:image"]/@src'
        data = response.xpath(regx).extract()
        meta['cover'] = ''
        if data:
            if (data[0].find('default') == -1):
                meta['cover'] = data[0].replace('spst', '\
lpst').replace('mpic', 'lpic')
            else:
                meta['cover'] = ''
        return meta

    def get_name(self, meta, response):
        regx = '//title/text()'
        data = response.xpath(regx).extract()
        if data:
            meta['name'] = data[0][:-5].strip()
        return meta

    def get_slug(self, meta, response):
        meta['slug'] = util.shorturl(meta['douban_id'])
        return meta

    def get_year(self, meta, response):
        regx = '//span[@class="year"]/text()'
        data = response.xpath(regx).extract()
        if data:
            meta['year'] = validator.match_year(data[0])
        return meta

    def get_directors(self, meta, response):
        regx = '//a[@rel="v:directedBy"]/text()'
        directors = response.xpath(regx).extract()
        meta['directors'] = validator.process_slash_str('/'.join(directors))
        return meta

    def get_director_ids(self, meta, response):
        regx = '//a[@rel="v:directedBy"]/@href'
        director_ids = response.xpath(regx).extract()
        director_ids = [ ids.split("/")[-2]for ids in director_ids]

        regx1 = '//a[@rel="v:directedBy"]/text()'
        directors = response.xpath(regx1).extract()

        cmb_directors = []
        for i in range(len(director_ids)):
            cmb_directors.append(directors[i] + ":" + director_ids[i])

        meta['director_ids'] = validator.process_slash_str('|'.join(cmb_directors))
        return meta

    def get_actors(self, meta, response):
        regx = '//a[@rel="v:starring"]/text()'
        actors = response.xpath(regx).extract()
        meta['actors'] = validator.process_slash_str('/'.join(actors))
        return meta

    def get_actor_ids(self, meta, response):
        regx = '//a[@rel="v:starring"]/@href'
        actor_ids = response.xpath(regx).extract()
        actor_ids = [ ids.split("/")[-2]for ids in actor_ids]

        regx1 = '//a[@rel="v:starring"]/text()'
        actors = response.xpath(regx1).extract()

        cmb_actor = []
        for i in range(len(actor_ids)):
            cmb_actor.append(actors[i] + ":" + actor_ids[i])

        meta['actor_ids'] = validator.process_slash_str('|'.join(cmb_actor))
        return meta

    def get_genres(self, meta, response):
        regx = '//span[@property="v:genre"]/text()'
        genres = response.xpath(regx).extract()
        meta['genres'] = '/'.join(genres)
        return meta

    def get_official_site(self, meta, response):
        regx = '//a[preceding-sibling::span[text()="官方网站:"]][following-si\
bling::br]/@href'
        data = response.xpath(regx).extract()
        if data:
            meta['official_site'] = validator.process_url(data[0])
        return meta

    def get_regions(self, meta, response):
        regx = '//text()[preceding-sibling::span[text()="制片国家/地区:"]][fo\
llowing-sibling::br]'
        data = response.xpath(regx).extract()
        if data:
            meta['regions'] = data[0]
        return meta

    def get_languages(self, meta, response):
        regx = '//text()[preceding-sibling::span[text()="语言:"]][following-s\
ibling::br]'
        data = response.xpath(regx).extract()
        if data:
            meta['languages'] = data[0]
        return meta

    def get_release_date(self, meta, response):
        regx = '//span[@property="v:initialReleaseDate"]/@content'
        data = response.xpath(regx).extract()
        if data:
            release_date = validator.str_to_date(validator.match_date(data[0]))
            if release_date:
                meta['release_date'] = release_date
        return meta

    def get_runtime(self, meta, response):
        regx = '//span[@property="v:runtime"]/@content'
        data = response.xpath(regx).extract()
        if data:
            meta['mins'] = data[0]
        return meta

    def get_alias(self, meta, response):
        regx = '//text()[preceding-sibling::span[text()="又名:"]][following-s\
ibling::br]'
        data = response.xpath(regx).extract()
        if data:
            meta['alias'] = validator.process_slash_str(data[0])
        return meta

    def get_imdb_id(self, meta, response):
        regx = '//a[preceding-sibling::span[text()="IMDb链接:"]][following-si\
bling::br]/@href'
        data = response.xpath(regx).extract()
        if data:
            meta['imdb_id'] = data[0].strip().split('?')[0][26:]
        return meta

    def get_score(self, meta, response):
        regx = '//strong[@property="v:average"]/text()'
        data = response.xpath(regx).extract()
        if data:
            meta['douban_score'] = data[0]
        return meta

    def get_votes(self, meta, response):
        regx = '//span[@property="v:votes"]/text()'
        data = response.xpath(regx).extract()
        if data:
            meta['douban_votes'] = data[0]
        return meta

    def get_tags(self, meta, response):
        regx = '//div[@class="tags-body"]/a/text()'
        tags = response.xpath(regx).extract()
        meta['tags'] = '/'.join(tags)
        return meta

    def get_comments(self, meta, response):
        regx = '//div[@class="comment"]/p/text()'
        comments = response.xpath(regx).extract()
        meta['comments'] = '/'.join((i.strip() for i in comments))
        return meta

    def get_storyline(self, meta, response):
        regx = '//span[@class="all hidden"]/text()'
        data = response.xpath(regx).extract()
        if data:
            meta['storyline'] = data[0]
        else:
            regx = '//span[@property="v:summary"]/text()'
            data = response.xpath(regx).extract()
            if data:
                meta['storyline'] = data[0]
        return meta

    def parse(self, response):
        print("=====================================+++++++++",response.url)
        if 35000 > len(response.body):
            print("movie.meta.response.body: ", response.body)
            print("movie.meta.response.url: ",response.url)
        elif 404 == response.status:
            print("movie.meta.response.url: ",response.url)
        else:
            meta = MovieMeta()
            self.get_douban_id(meta, response)
            self.get_type(meta, response)
            self.get_cover(meta, response)
            self.get_name(meta, response)
            self.get_year(meta, response)
            self.get_directors(meta, response)
            self.get_actors(meta, response)
            self.get_genres(meta, response)
            self.get_official_site(meta, response)
            self.get_regions(meta, response)
            self.get_languages(meta, response)
            self.get_release_date(meta, response)
            self.get_runtime(meta, response)
            self.get_alias(meta, response)
            self.get_imdb_id(meta, response)
            self.get_score(meta, response)
            self.get_votes(meta, response)
            self.get_tags(meta, response)
            self.get_storyline(meta, response)
            self.get_actor_ids(meta, response)
            self.get_director_ids(meta, response)
            self.get_slug(meta, response)
            return meta

    def second_parse(self,response):
        """print user-agent"""
        print("\nChange User-Agent: ", response.request.headers['User-Agent'])
