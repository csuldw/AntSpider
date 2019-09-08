---
layout: page
homepage: true
title: 数据集使用说明
---

# 数据集概况

本数据集采集于豆瓣电影，电影与明星数据收集于2019年8月上旬，影评数据(用户、评分、评论)收集于2019年9月初，共945万数据，其中包含14万部电影，7万演员，63万用户，416万条电影评分，442万条影评，该数据集正好弥补下国内公开电影​数据集的空缺。数据已经过初步清洗，可用于推荐系统、情感分析、QA问答、知识图谱等多个领域。

数据集共有5个文件: movies.csv、person.csv、users.csv、comments.csv、ratings.csv，关于各个文件的具体内容将在下文介绍。


# 使用许可

该数据集只为方便各位研究人员，**如涉及侵犯个人或团体利益，请与我们联系，我们将主动撤销一切相关数据，谢谢**！

数据使用需遵循[豆瓣使用协议 & 豆瓣隐私政策](https://accounts.douban.com/passport/agreement),

该数据集仅限用于研究目的，我们不能保证数据的正确性以及任何场景的适用性。对于使用这份数据的用户，必须严格遵循下列条件: 

1. 未经许可，用户不得将此数据集用于任何商业或收入交易用途。
2. 未经单独许可，用户不得重新转发数据。
3. 用户在使用数据集时，必须声明数据来源。



在任何情况下，我们均不对因使用这些数据而造成的任何损失承担责任（包括但不限于数据丢失或数据不准确）。如果您有任何其他问题或意见，请发送电子邮件至: csu.ldw@csu.edu.cn


# 数据格式

## Movie数据格式

电影数据共140502部，2019年之前的电影有139129，当前未上映的有1373部，包含21个字段，部分字段数据为空，字段说明如下: 

- MOVIE_ID: 电影ID，对应豆瓣的DOUBAN_ID
- NAME: 电影名称
- ALIAS: 别名
- ACTORS: 主演
- COVER: 封面图片地址
- DIRECTORS: 导演
- GENRES: 类型
- OFFICIAL_SITE: 官方地址
- REGIONS: 制片国家/地区
- LANGUAGES: 语言
- RELEASE_DATE: 上映日期
- MINS: 片长
- IMDB_ID: IMDbID
- DOUBAN_SCORE: 豆瓣评分
- DOUBAN_VOTES: 豆瓣投票数
- TAGS: 标签
- STORYLINE: 电影描述
- SLUG: 加密的url，可忽略
- YEAR: 年份
- ACTOR_IDS: 演员与PERSON_ID的对应关系,多个演员采用“\|”符号分割，格式“演员A:ID\|演员B:ID”；
- DIRECTOR_IDS: 导演与PERSON_ID的对应关系,多个导演采用“\|”符号分割，格式“导演A:ID\|导演B:ID”；

## Person数据格式

Person文件只包括演员和导演，不包含豆瓣用户数据，共72959个名人数据，包含10个字段，每个PERSON_ID都会对应一个name，不存在PERSON_ID的数据已过滤，各个字段说明如下: 

- PERSON_ID: 名人ID
- NAME: 演员名称
- SEX: 性别
- NAME_EN: 更多英文名
- NAME_ZH: 更多中文名
- BIRTH: 出生日期
- BIRTHPLACE: 出生地
- CONSTELLATORY: 星座
- PROFESSION: 职业
- BIOGRAPHY: 简介，存在简介数据的名人只有15135个。


## User数据格式

users.csv数据为豆瓣用户的脱敏信息，主要是与评论和评分绑定在一起，共获取了639125用户数据，包含2个字段（已删除两个），具体的字段如下：

- USER_MD5：USER_ID加密的MD5,去敏处理
- USER_NICKNAME: 评论用户昵称
- ~~USER_AVATAR: 评论用户头像~~（已删除）
- ~~USER_URL: 评论用户url~~（已删除）


## Rating数据格式

评分数据从评论数据中获得，由于豆瓣限制了未登录用户查看的数据量，所以每部电影最多320个评分，最终得到600384个用户的4169420条评分数据，涉及电影68471部，评分值为1-5分（1-很差，2-较差，3-还行，4-推荐，5-力荐），共包含5个字段，数据格式如下：

- RATING_ID: 评分ID
- USER_MD5：USER_ID加密的MD5
- MOVIE_ID: 电影ID，对应豆瓣的DOUBAN_ID
- RATING: 评分
- RATING_TIME: 评分时间


## Comment数据格式

评论数据共4428475 条，用户638963个，电影68887包含7个字段，各个字段说明如下: 

- COMMENT_ID: 评论ID
- USER_MD5：USER_ID加密的MD5
- MOVIE_ID: 电影ID，对应豆瓣的DOUBAN_ID
- CONTENT: 评论内容
- VOTES: 评论赞同数
- RATINGS: 评论携带的分数
- COMMENT_TIME: 评论时间

# 下载地址

样例数据每个文件1000条数据，下载地址：[moviedata_small.tar.gz](http://moviedata.csuldw.com/dataset/moviedata_small.tar.gz)。完整的数据集有1G+，需要的用户可以点击后面的链接进行下载：[moviedata-10m.tar.gz](https://pan.baidu.com/s/1YdCTPOcnowJuP5XZrjOiVA)，密码获取方式如下(不定期更换): 


1. 微信搜索**【斗码小院】**公众号并点击关注;
2. 后台回复**【电影数据集】**获取密码.

数据采集不易，为了初步了解多少人使用该数据，还请各位使用人员不要进行二次转发！"授人以鱼不如授人以渔"，
如果您对爬虫技术感兴趣，可前往Github参考笔者的[AntSpider](https://github.com/csuldw/AntSpider)项目源码。如果数据对您有用，可关注下公众号[斗码小院](http://www.csuldw.com/assets/articleImg/2019/code-main-fun.png)，里面有数据收集、数据处理、数据建模等多篇文章，您的关注就是对我们最好的支持，另外，还可以在下方的Github的Star中点击一下。


# 相关数据集推荐

之前也有用户公开过豆瓣电影数据，这里提供下链接给大家参考下，同时提供一下movielens电影数据集的下载地址：

1. [Douban Movie Short Comments Dataset](https://www.kaggle.com/utmhikari/doubanmovieshortcomments)
2. [豆瓣电影评分数据集](https://www.kesci.com/home/dataset/58acf6f1d2445916845b4033)
3. [movielens-dataset](https://grouplens.org/datasets/movielens/)

# Contributor

<!-- [MIT](LICENSE) &copy;  -->
1. [Diwei Liu](http://www.csuldw.com)
2. [Yong Gao]()
3. [Yina Xu]()

