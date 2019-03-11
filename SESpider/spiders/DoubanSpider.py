import scrapy


class DoubanSpider(scrapy.Spider):
    name = "doubanSpider"
    allowed_domains = ["movie.douban.com"]
    start_urls = ['https://movie.douban.com/tag/#/']

    def parse(self, response):
        for index in range(0,100,10):
            movie_url = 'https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=&start={1}'.format(index)
            print(movie_url)

if __name__ == '__main__':
    DoubanSpider.parse()
