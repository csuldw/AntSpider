#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  4 16:11:58 2019

@author: liudiwei
"""

import requests
import json
import math
import database as db
cursor = db.connection.cursor()
import time

MAX_SIZE = 100

def get_new_ip(num):
    url = ""#代理商的IP连接，Get请求，返回结果为“|”连接的IP
    time.sleep(1)
    return requests.get(url).text.strip().split("|")

def get_ip_list(num):
    """
    [{'expire_time': '2019-09-02 20:30:25',
      'ip': '119.142.205.84',
      'port': '4341'}]
    """
    url = ""#代理商的IP连接，Get请求，返回结果为上面的数组
    ip_list = json.loads(requests.get(url).text)["data"]
    print("ip_list",ip_list)
    return ip_list
    
def check_ip_valid(ip):
    time.sleep(1)
    url = "" #代理商判断IP是否有效
    text = requests.get(url, verify=False).text
    result = json.loads(text)["data"][ip]
    print("check result: ",result)
    return result

#sql = "SELECT * FROM update_proxy_new.pyproxys where valid = 1"
#cursor.execute(sql)
#cursor.fetchone()


def save_proxy(proxy, expire_time=None):
    keys = ["proxy_ip"]
    if expire_time:
        keys.append("valid_time")
        
    fields = ','.join(keys)
    
    if expire_time:
        
        sql = 'INSERT INTO proxys (%s) VALUES ("%s","%s")' % (fields, proxy, expire_time)
    else:
        sql = 'INSERT INTO proxys (%s) VALUES (%s)' % (fields, proxy)
    print(sql)
    cursor.execute(sql)
    return db.connection.commit()

def update_proxy_as_invalid(proxy_ip):
    sql = 'UPDATE proxys SET valid=0 WHERE proxy_ip="%s"' % (proxy_ip)
    cursor.execute(sql)
    return db.connection.commit()

def get_proxy():
    sql = "SELECT DISTINCT(proxy_ip) FROM proxys where valid = 1 "
    cursor.execute(sql)
    all_proxy = cursor.fetchall()
    proxy_list = []
    for proxy in all_proxy:
        ip = proxy["proxy_ip"]
        proxy_list.append(ip)
    return proxy_list


def get_valid_proxy():
    sql = "SELECT DISTINCT(proxy_ip) FROM proxys where valid=1 and CURRENT_TIME<proxys.valid_time"
    cursor.execute(sql)
    all_proxy = cursor.fetchall()
    proxy_list = []
    for proxy in all_proxy:
        ip = proxy["proxy_ip"]
        proxy_list.append(ip)
    return proxy_list


def quick_proxy():
    proxy_list = get_proxy()
    
    for proxy_ip in proxy_list:
        if check_ip_valid(proxy_ip) == False:
            print("proxy %s is invalid." % proxy_ip)
            proxy_list.remove(proxy_ip)
            update_proxy_as_invalid(proxy_ip)
    
    print("valid ip size: ", len(proxy_list) )
    while len(proxy_list) < MAX_SIZE:

        ip_num = MAX_SIZE - len(proxy_list)
        print("ip_num: ", ip_num, ",proxy_list size:", len(proxy_list))
        print("get new ip...")
        new_proxy_list = get_new_ip(ip_num)
        print(new_proxy_list)
        #new_proxy_list = "113.121.177.23:19454|183.166.125.208:21600|106.117.130.29:20899|117.62.60.178:21562|27.159.167.179:18971|49.76.54.145:15854|1.199.185.178:17846|61.186.65.66:20339|115.210.182.8:21258|121.61.0.223:22551".split("|")
        for new_proxy in new_proxy_list:
            if new_proxy not in proxy_list:
                proxy_list.append(new_proxy)
                print("new proxy ip:", new_proxy)
                save_proxy(new_proxy)
    print("detect finished!")
            
def update_valid_proxy():
    sql = 'UPDATE proxys SET valid=0 WHERE CURRENT_TIME>proxys.valid_time'
    cursor.execute(sql)
    
    #sql = 'UPDATE proxys SET valid=0 WHERE proxy_ip in (select proxy_ip from (select proxy_ip,call_times,created_time from proxys where valid=1 order by call_times desc,created_time desc limit 10) as a)'
    cursor.execute(sql)
    
    sql = 'UPDATE proxys SET call_times=0 WHERE valid=1'
    cursor.execute(sql)
    return db.connection.commit()

if __name__ == '__main__':
    update_valid_proxy()
    proxy_list = get_valid_proxy()
    
    print("valid ip size: ", len(proxy_list) )
    
    if len(proxy_list) < MAX_SIZE:
        ip_num = 10 + int(math.fabs(MAX_SIZE - len(proxy_list)))
        print("ip_num: ", ip_num, ",proxy_list size:", len(proxy_list))
        
        print("get new ip...")
        new_proxy_list = get_ip_list(ip_num)
        print(new_proxy_list)
        for new_proxy in new_proxy_list:
            expire_time = new_proxy["expire_time"]
            proxy_ip_item = new_proxy["ip"] + ":" + new_proxy["port"]
            if proxy_ip_item not in proxy_list:
                proxy_list.append(proxy_ip_item)
                print("new proxy ip:", proxy_ip_item)
                
                save_proxy(proxy_ip_item, expire_time)
    
    print("detect finished!")
    
