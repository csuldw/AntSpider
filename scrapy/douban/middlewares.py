# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random
from scrapy import signals
from twisted.internet.error import TimeoutError
from douban.util import AGENT_LIST,PRIVATE_PROXY,init_proxy,check_ip_valid,get_new_ip,get_proxy
from douban.proxylib import ProxyTool
import base64
import douban.database as db


proxy_tool = ProxyTool()

class DoubanSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        print(f'#return exception reason：{type(exception)}')
        #if isinstance(exception,TimeoutError):
        #    spider.logger.info("Request TimeoutError.")
            #return request
        #spider.logger.info('exception: %s' % spider.name)
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class DoubanDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class DepthMiddleware(object):

    def __init__(self, maxdepth, stats=None, verbose_stats=False, prio=1):
        self.maxdepth = maxdepth
        self.stats = stats
        self.verbose_stats = verbose_stats
        self.prio = prio

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        maxdepth = settings.getint('DEPTH_LIMIT')
        verbose = settings.getbool('DEPTH_STATS_VERBOSE')
        prio = settings.getint('DEPTH_PRIORITY')
        return cls(maxdepth, crawler.stats, verbose, prio)

    def process_spider_output(self, response, result, spider):
        def _filter(request):
            if isinstance(request, Request):
                depth = response.meta['depth'] + 1
                request.meta['depth'] = depth
                if self.prio:
                    request.priority -= depth * self.prio
                if self.maxdepth and depth > self.maxdepth:
                    logger.debug(
                        "Ignoring link (depth > %(maxdepth)d): %(requrl)s ",
                        {'maxdepth': self.maxdepth, 'requrl': request.url},
                        extra={'spider': spider}
                    )
                    return False
                elif self.stats:
                    if self.verbose_stats:
                        self.stats.inc_value('request_depth_count/%s' % depth,
                                             spider=spider)
                    self.stats.max_value('request_depth_max', depth,
                                         spider=spider)
            return True

        # base case (depth=0)
        if self.stats and 'depth' not in response.meta:
            response.meta['depth'] = 0
            if self.verbose_stats:
                self.stats.inc_value('request_depth_count/0', spider=spider)

        return (r for r in result or () if _filter(r))

class ProxyMiddleware(object):
    def process_request(self, request, spider):
        
        # curl https://m.douban.com/book/subject/26628811/ -x http://127.0.0.1:8081
        #request.meta['proxy'] = 'http://27.43.187.24:9999'
        cursor = db.connection.cursor()
        sql = "SELECT proxy_ip,call_times FROM proxys where valid = 1 order by call_times limit 2"
        print("\n\n###SQL:", sql)

        cursor.execute(sql)
        all_proxy = cursor.fetchall()
        proxy_list = []
        for proxy in all_proxy:
            ip = proxy["proxy_ip"]
            proxy_list.append(ip)  

        PROXY_LIST = proxy_list
        #PROXY_LIST = get_proxy()
        print("=======###PROXY INFO: ", len(PROXY_LIST), PROXY_LIST)
        proxy_ip = random.choice(PROXY_LIST)

        #将mysql调用次数+1
        sql = 'UPDATE proxys SET call_times=call_times+1 WHERE proxy_ip="%s"' % (proxy_ip)
        cursor.execute(sql)
        db.connection.commit()
        cursor.close()

        # 设置代理的认证信息
        #auth = base64.b64encode(bytes("136756895:g9zaye1k", 'utf-8'))
        #request.headers['Proxy-Authorization'] = b'Basic ' + auth
        #proxy_ip = "58.255.207.22:19783"
        ##private proxy
        if PRIVATE_PROXY:
            # proxy = "http://136756895:g9zaye1k@" + proxy_ip
            proxy = "http://" + proxy_ip
        else:
            proxy = "http://" + proxy_ip
        spider.logger.info("\n==================proxy===================")
        spider.logger.info("Switch proxy ip: %s"  % proxy)

        request.meta['proxy'] = proxy

        # request.meta['proxy'] = 'http://10.0.0.164:1080'

class RandomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        user_agent  = random.choice(AGENT_LIST)
        if user_agent:
            request.headers.setdefault('User-Agent', user_agent)
