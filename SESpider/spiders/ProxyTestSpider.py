import scrapy
import json
from scrapy.selector import Selector
class ProxyTestSpider(scrapy.Spider):
    name = "ProxyTestSpider"
    allowed_domains = ["ip.cn"]
    start_urls = ['https://ip.cn/']
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            # 'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'SESpider.middlewares.ProcessAllExceptionMiddleware': 120,
            'SESpider.middlewares.RandomProxyMiddleware': 100,
        },
        'DOWNLOAD_DELAY': 1,  # 延时最低为2s
        'AUTOTHROTTLE_ENABLED': True,  # 启动[自动限速]
        'AUTOTHROTTLE_DEBUG': True,  # 开启[自动限速]的debug
        'AUTOTHROTTLE_MAX_DELAY': 10,  # 设置最大下载延时
        'DOWNLOAD_TIMEOUT': 15,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 4  # 限制对该网站的并发请求数

    }
    def parse(self, response):
        selector = Selector(text=response.text)
        print(selector.xpath('//*').extract())

        # test_url = 'http://ip.filefab.com/'

