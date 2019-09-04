#!/bin/sh

ps -ef | grep scrapy | grep -v grep | grep 'movie_comment' | cut -c 6-12 | xargs kill -9

cd /Users/liudiwei/github/SwiftQA/AntSpider/scrapy

/Users/liudiwei/anaconda3/bin/python /Users/liudiwei/anaconda3/bin/scrapy crawl movie_comment
