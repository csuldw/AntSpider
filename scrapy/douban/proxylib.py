#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 23:41:38 2019

@author: liudiwei
"""

import requests
import re
import random
import codecs
from urllib import parse
 
 
class ProxyTool(object):
    """
    代理类
    """
    def __init__(self):
        self.headers = {"User-Agent": "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11"}
        pass
 
    def get_user_agent(self):
        """
        得到随机user-agent
        :return:
        """
        user_agents = [
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
            "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
            "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
            "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
            "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
            "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
            "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
            "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
        ]

        user_agent = random.choice(user_agents)
        return user_agent
 
 
    def get_proxy(self, choice='http', first=1, end=2):
        """
        获取代理
        :param choice:
        :param first: 开始爬取的页数
        :param end: 结束爬取的后一页
        :return:
        """
 
        ip_list = []
        base_url = None
        if choice == 'http':
            base_url = 'http://www.xicidaili.com/wt/'
        elif choice == 'https':
            base_url = 'http://www.xicidaili.com/wn/'
 
        for n in range(first, end):
            actual_url = base_url + str(n)
            html = requests.get(url=actual_url, headers=self.headers).text
            pattern = '(\d+\.\d+\.\d+\.\d+)</td>\s*<td>(\d+)'
            re_list = re.findall(pattern, html)
 
            for ip_port in re_list:
                ip_port = ip_port[0] + ':' + ip_port[1]
                ip_list.append(ip_port)
        return ip_list
 
 
    def test_proxy(self, ip_port, choice='http'):
        """
        测试代理是否能用
        :param ip_port:
        :param choice:
        :return:
        """
        proxies = None
        # 这个网站可以返回你公网下的IP，如果你加代理请求后，返回的就是你代理的IP（这样做是防止你虽然用的是代理IP，但实际是用你自己的公网IP访问的请求）
        tar_url = "http://icanhazip.com/"
        user_agent = self.get_user_agent()
        headers = {'User-Agent': user_agent}
        if choice == 'http':
            proxies = {
                "http": "http://"+ip_port,
            }
 
        elif choice == 'https':
            proxies = {
                "https": "https://" + ip_port,
            }
        try:
            thisIP = "".join(ip_port.split(":")[0:1])
            res = requests.get(tar_url, proxies=proxies, headers=headers, timeout=8)
            proxyIP = res.text.strip()
            if proxyIP == thisIP:
                return proxyIP
            else:
                return False
        except:
            return False
 
#    def store_txt(self, choice='http', first=1, end=2):
#        """
#        将测试通过的ip_port保存为txt文件
#        :param choice:
#        :param first:
#        :param end:
#        :return:
#        """
#        user_agent = self.get_user_agent()
#        headers = {'User-Agent': user_agent}
#        ip_list = self.get_proxy(headers=headers, choice=choice, first=first, end=end)
#        with codecs.open("Http_Agent.txt", 'a', 'utf-8') as file:
#            for ip_port in ip_list:
#                ip_port = self.test_proxy(ip_port, choice=choice)
#                print(ip_port)
#                if ip_port:
#                    file.write('\'' + ip_port + "\'\n")
                    
                    
import json
def check_ip_valid(ip):
    url = "https://dps.kdlapi.com/api/checkdpsvalid?orderid=966475943170494&signature=gu0yhmscwn5jva218dliy9gs6xg3oqov&proxy=" + ip
    text = requests.get(url).text
    result = json.loads(text)["data"][ip]
    return result


if __name__ == "__main__":
    with open("proxy.txt") as fr:
        ip_list = fr.readlines()
        
    ip_list = [ip.strip() for ip in ip_list]
    
    proxy = ProxyTool()
    ip_list = proxy.get_proxy()
    good_ip = []
    for ip in ip_list:
        print("Start to test ip:", ip)
        ip_test_res = proxy.test_proxy(ip)
        if ip_test_res:
            print("Yes:", ip)
            good_ip.append(ip)