#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 23:41:38 2019

@author: liudiwei
"""

import pymysql

MYSQL_DB = 'douban'
MYSQL_USER = 'root'
MYSQL_PASS = 'gedahippo'
MYSQL_HOST = 'localhost'

connection = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER,
                             password=MYSQL_PASS, db=MYSQL_DB,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
