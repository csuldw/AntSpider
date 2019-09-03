

"""
id，电影名称，豆瓣评分，评分人数，上映时间，导演，主演，制片国家，影片简介
"""

import urllib.request as urlrequest
from bs4 import BeautifulSoup
import re
import csv,codecs 

top250_url ='https://movie.douban.com/top250?start={}&filter='
movie_name='名称'
movie_assess='评价人数'
movie_score='评分'
movie_url ='链接'
movie_intro='介绍'
movie_num =0

#print('{} {} {} {} {}'.format(movie_name,movie_assess,movie_score,movie_url,movie_intro))
with open('top250_movie.csv','w',encoding='utf8') as outputfile:
    #outputfile.write(codecs.BOM_UTF8)
    writer = csv.writer(outputfile)
    #writer.writerow(["movie_num","movie_name","movie_assess","movie_score","movie_url","movie_intro"])
    outputfile.write("movie_num#movie_name#movie_year#movie_country#movie_type#movie_director#movie_assess#movie_score#movie_url#movie_intro\n")
    for list in range(10):
             movies_content = urlrequest.urlopen(top250_url.format(list*25)).read()
             movies_html = movies_content.decode('utf8')
             moviessoup = BeautifulSoup(movies_html,'html.parser')
             all_list = moviessoup.find_all(class_='item')
             #print(all_list)
             for item in all_list:
                 item_data=item.find(class_='pic')
                 movie_url = item_data.find('a')['href']
                 movie_name = item_data.find('img')['alt']
                 item_info = item.find(class_='star')
                 info = item.find('div', attrs={'class': 'star'})
                #find_all 将star标签中的所有span 存入一个列表中
                 movie_assess =info.find_all('span')[3].get_text()[:-3]
                 movie_score = item_info.find('span',attrs={'class':'rating_num'}).get_text()
                 try:
                     movie_intro = item.find(class_='quote').find(class_='inq').get_text()
                 except Exception as e:
                     movie_intro='None'  
                        
                 movie_num =movie_num+1
                 #print(movie_assess)
                 #print(item_assissent)
                 # item_assisent = item_data.find(name='span',attrs={'property':'v:average'})
                
                 #抓取电影上映年份、 导演、主演等信息
                 movie_actor_infos_html = item.find(class_='bd')
                 #strip() 方法用于移除字符串头尾指定的字符（默认为空格）
                 movie_actor_infos = movie_actor_infos_html.find('p').get_text().strip().split('\n')
                 actor_infos1 = movie_actor_infos[0].split('\xa0\xa0\xa0')
                 movie_director = actor_infos1[0][3:]
                 #print(movie_director)
                 movie_role = movie_actor_infos[1]
                
                 movie_year_area = movie_actor_infos[1].lstrip().split('\xa0/\xa0')
                 movie_year = movie_year_area[0]
                 #print(movie_year)
                 movie_country = movie_year_area[1]
                 #print(movie_country)
                 
                 movie_type = movie_year_area[2]
                 #print(movie_type)
                    
                 #print('{} {} {} {} {} {} {} {} {} {}'.format(movie_num,movie_name,movie_year,movie_country,movie_type,movie_director,movie_assess,movie_score,movie_url,movie_intro))
                
                 #writer.writerow([movie_num,movie_name,movie_assess,movie_score,movie_url,movie_intro])

                 if movie_type =='':
                    movie_type='NULL'
                     
                 outputfile.write('{}#{}#{}#{}#{}#{}#{}#{}#{}#{}\n'.format(movie_num,movie_name,movie_year,movie_country,movie_type,movie_director,movie_assess,movie_score,movie_url,movie_intro))
                      