## 豆瓣爬虫说明

scrapy目录为爬虫的核心，爬虫基于scrapy框架，各个目录和文件的说明如下：

1. douban: 豆瓣爬虫
	1. spiders: 存放你Spider文件，也就是你爬取的py文件
		- 电影相关
			- movie_comment.py：电影评论
			- movie_meta.py：电影详情信息
			- movie_subject: 电影的douban_id爬取；
		- 书籍相关
			- book_coment.py: 书籍评论爬虫
			- book_meta：获取书籍信息
			- book_subject:获取书籍的douban_id
		- 名人
			- person_meta.py：名人信息爬取
	3. douban/items.py：相当于一个容器，和字典较像。
	4. douban/middlewares.py：定义Downloader Middlewares(下载器中间件)和Spider Middlewares(中间件)的实现。
	5. douban/pipelines.py:定义Item Pipeline的实现，实现数据的清洗，储存，验证。
	6. douban/settings.py：全局配置文件。
	7. douban/util.py: 独立的工具类文件。
	8. douban/validator.py: 用于校验数据的附加文件.
	9. douban/update_proxy.py：用于更新数据库代理的文件。
	10. douban/rebuild_pid.py: 将movie中的actor_ids和director_ids转存到person_obj表中.
2. sql: sql语句
3. scrapy.cfg：配置文件。
4. 三个shell文件为笔者自己部署爬虫的时候编写的，可忽略。


## 添加cookie的三种方式

### settings

去掉`settings.py`文件Cookies_enabled=False的注释，settings的headers配置的cookie就可以用了这种方法最简单，同时cookie可以直接粘贴浏览器的。后两种方法添加的cookie是字典格式的，需要用json反序列化一下,而且需要设置settings中的Cookies_enabled=True

### DownloadMiddleware

settings中给downloadmiddleware解注释
去中间件文件中找downloadmiddleware这个类，修改process_request，添加request.cookies={}即可。

### 爬虫主文件中重写start_request

```
def start_requests(self):
    yield scrapy.Request(url,dont_filter=True,cookies={自己的cookie})
```

