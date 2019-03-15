import scrapy
import json
import re
import hashlib
from SESpider.items import DyttMovieItem,MovieItemLoader
from SESpider.settings import USER_AGENT
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule
from scrapy.selector import Selector
def get_md5(url):
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


class DyttMovieSpider(CrawlSpider):
    name = "DyttMovieSpider"
    allowed_domains = ["dytt8.net"]
    start_urls = ['http://www.dytt8.net']

    rules = (
        Rule(LinkExtractor(allow=("html/gndy/.*/\d+/\d+.html",)),callback='parse_movie',follow=True),
    )

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'SESpider.middlewares.ProcessAllExceptionMiddleware': 110,
            'SESpider.middlewares.RandomProxyMiddleware': None,
        },
        "USER_AGENT": USER_AGENT,
        'DOWNLOAD_DELAY': 5,  # 延时最低为2s
        'AUTOTHROTTLE_ENABLED': True,  # 启动[自动限速]
        'AUTOTHROTTLE_DEBUG': True,  # 开启[自动限速]的debug
        'AUTOTHROTTLE_MAX_DELAY': 10,  # 设置最大下载延时
        'DOWNLOAD_TIMEOUT': 15,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 4  # 限制对该网站的并发请求数

    }
    def parse_movie(self, response):
        selector = Selector(text=response.text)
        try:
            movie_cover = selector.xpath('//div[@id="Zoom"]//p[1]/img/@src').extract()[0]
        except:
            return
        try:
            movie_title_translate = re.match('◎译　　名　(.*)?',selector.xpath('//div[@id="Zoom"]//p[1]/text()').extract()[2]).group(1)
            movie_title_origin = re.match('◎片　　名　(.*)?',selector.xpath('//div[@id="Zoom"]//p[1]/text()').extract()[3]).group(1)
        except:
            try:
                movie_title_translate = re.match('◎译　　名　(.*)?',selector.xpath('//div[@id="Zoom"]//p[1]/text()').extract()[1]).group(1)
                movie_title_origin = re.match('◎片　　名　(.*)?',selector.xpath('//div[@id="Zoom"]//p[1]/text()').extract()[2]).group(1)
            except:
                try:
                    movie_title_origin = re.match('◎片　　名　(.*)?',selector.xpath('//div[@id="Zoom"]//p[1]/text()').extract()[2]).group(1)
                    movie_title_translate = re.match('◎译　　名　(.*)?',selector.xpath('//div[@id="Zoom"]//p[1]/text()').extract()[3]).group(1)
                except:
                    movie_title_origin = re.match('◎片　　名　(.*)?',selector.xpath('//div[@id="Zoom"]//p[1]/text()').extract()[1]).group(1)
                    movie_title_translate = re.match('◎译　　名　(.*)?',selector.xpath('//div[@id="Zoom"]//p[1]/text()').extract()[2]).group(1)
        movie_title = movie_title_translate + ' ' + movie_title_origin
        try:
            movie_download_url = selector.xpath('//div[@id="Zoom"]//a/text()').extract()[0]
        except:
            movie_download_url = selector('//div[@id="Zoom"]//td[@style="WORD-WRAP: break-word"]/text()').extract()[0]

        dyttMovieItemLoader = MovieItemLoader(item=DyttMovieItem(),response=response)

        dyttMovieItemLoader.add_value("movie_id",get_md5(response.url))
        dyttMovieItemLoader.add_value("movie_title",movie_title)
        dyttMovieItemLoader.add_value("movie_download_url",movie_download_url)
        dyttMovieItemLoader.add_value('movie_url',response.url)
        dyttMovieItemLoader.add_value('movie_cover',movie_cover)

        dyttMovieItem = dyttMovieItemLoader.load_item()
        yield  dyttMovieItem


if __name__ == '__main__':
    pass