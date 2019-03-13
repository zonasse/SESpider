from scrapy.cmdline import execute
import sys
import os
from SESpider.tools.crawl_ip_tool import crawl_ip_list
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# crawl_ip_list()
execute(["scrapy", "crawl", "DoubanMovieSpider"])
# execute(["scrapy","crawl","ProxyTestSpider"])
