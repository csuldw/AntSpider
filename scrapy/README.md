Scrapy文件说明：


1. scrapy.cfg：配置文件
2. spiders：存放你Spider文件，也就是你爬取的py文件
3. items.py：相当于一个容器，和字典较像
4. middlewares.py：定义Downloader Middlewares(下载器中间件)和Spider Middlewares(蜘蛛中间件)的实现
5. pipelines.py:定义Item Pipeline的实现，实现数据的清洗，储存，验证。
6. settings.py：全局配置


## 添加cookie的方式

1.settings
settings文件中给Cookies_enabled=False解注释
settings的headers配置的cookie就可以用了
这种方法最简单，同时cookie可以直接粘贴浏览器的。
后两种方法添加的cookie是字典格式的，需要用json反序列化一下,
而且需要设置settings中的Cookies_enabled=True

2.DownloadMiddleware
settings中给downloadmiddleware解注释
去中间件文件中找downloadmiddleware这个类，修改process_request，添加request.cookies={}即可。

3.爬虫主文件中重写start_request

```
def start_requests(self):
    yield scrapy.Request(url,dont_filter=True,cookies={自己的cookie})
```
