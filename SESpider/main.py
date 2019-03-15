from scrapy.cmdline import execute
import sys
import os
from SESpider.tools.crawl_ip_tool import crawl_ip_list
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# crawl_ip_list()
# execute(["scrapy", "crawl", "DoubanMovieSpider"])
# execute(["scrapy", "crawl", "DyttMovieSpider"])

# execute(["scrapy","crawl","ProxyTestSpider"])

from scrapy.crawler import CrawlerProcess
from SESpider.spiders import DoubanMovieSpider,DyttMovieSpider,ProxyTestSpider
from scrapy.utils.project import get_project_settings
process = CrawlerProcess(get_project_settings())
process.crawl(DoubanMovieSpider.DoubanMovieSpider)
process.crawl(DyttMovieSpider.DyttMovieSpider)
process.start()