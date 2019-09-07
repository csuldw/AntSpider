#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 23:41:38 2019

@author: liudiwei
"""

from scrapy import Item, Field


class Subject(Item):
    douban_id = Field()
    type = Field()


class MovieMeta(Item):
    douban_id = Field()
    type = Field()
    cover = Field()
    name = Field()
    slug = Field()
    year = Field()
    directors = Field()
    actors = Field()
    genres = Field()
    official_site = Field()
    regions = Field()
    languages = Field()
    release_date = Field()
    mins = Field()
    alias = Field()
    imdb_id = Field()
    douban_id = Field()
    douban_score = Field()
    douban_votes = Field()
    tags = Field()
    storyline = Field()
    actor_ids = Field()
    director_ids = Field()


class BookMeta(Item):
    douban_id = Field()
    slug = Field()
    name = Field()
    sub_name = Field()
    alt_name = Field()
    cover = Field()
    summary = Field()
    authors = Field()
    author_intro = Field()
    translators = Field()
    series = Field()
    publisher = Field()
    publish_date = Field()
    pages = Field()
    price = Field()
    binding = Field()
    isbn = Field()
    douban_id = Field()
    douban_score = Field()
    douban_votes = Field()
    tags = Field()


class Comment(Item):
    douban_id = Field()
    douban_comment_id = Field()
    douban_user_nickname = Field()
    douban_user_avatar = Field()
    douban_user_url = Field()
    content = Field()
    votes = Field()
    rating = Field()
    comment_time = Field()

class PersonMeta(Item):
    person_id = Field()
    name = Field()
    sex = Field()
    birth = Field()
    death = Field()
    birthplace = Field()
    biography = Field()
    profession = Field()
    constellatory = Field()
    name_zh = Field()
    name_en = Field()
