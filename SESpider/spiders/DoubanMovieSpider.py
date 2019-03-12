import scrapy
import json
import pickle
from SESpider.items import DoubanMovieItem,DoubanMovieItemLoader

class DoubanMovieSpider(scrapy.Spider):
    name = "DoubanMovieSpider"
    allowed_domains = ["movie.douban.com"]
    start_urls = ['https://movie.douban.com/tag/#/']

    def parse(self, response):
        for index in range(0,100,10):
            movie_url = 'https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=&start={}'.format(index)
            yield scrapy.Request(movie_url,callback=self.parse_main)

    def parse_main(self,response):
        movie_infos = json.loads(response.body.decode('utf-8'))
        movie_datas = movie_infos['data']
        for movie_data in movie_datas:
            doubanMovieItemLoader = DoubanMovieItemLoader(item=DoubanMovieItem(),response=response)
            movie_directors = ",".join(movie_data['directors'])
            movie_rate = movie_data['rate']
            movie_star = movie_data['star']
            movie_title = movie_data['title']
            movie_url = movie_data['url']
            movie_casts = ",".join(movie_data['casts'])
            movie_cover = movie_data['cover']
            movie_id = int(movie_data['id'])
            doubanMovieItemLoader.add_value("movie_directors",movie_directors)
            doubanMovieItemLoader.add_value("movie_rate",movie_rate)
            doubanMovieItemLoader.add_value("movie_star",movie_star)
            doubanMovieItemLoader.add_value("movie_title",movie_title)
            doubanMovieItemLoader.add_value("movie_url",movie_url)
            doubanMovieItemLoader.add_value("movie_casts",movie_casts)
            doubanMovieItemLoader.add_value("movie_cover",movie_cover)
            doubanMovieItemLoader.add_value("movie_id",movie_id)
            doubanmovieItem = doubanMovieItemLoader.load_item()
            # yield doubanmovieItem
            if movie_url:
                yield scrapy.Request(movie_url,callback=self.parse_detail,meta={'movie_id':movie_id,'item':doubanmovieItem})

    def parse_detail(self,response):
        movie_id = response.meta['movie_id']
        item = response.meta['item']
        base_url = 'https://movie.douban.com/subject/{}/comments?'.format(movie_id)
        # 全部评论
        all_comments_url = 'https://movie.douban.com/subject/{}/comments?status=P'.format(movie_id)
        # 前20条评论
        twenty_comments_url = 'https://movie.douban.com/subject/{}/comments?start=0&limit=20&sort=new_score&status=P'.format(movie_id)

        movie_abstract = response.xpath('//span[@property="v:summary"]/text()').extract()[0].strip()
        #提取简介
        item['movie_abstract'] = movie_abstract
        yield item
        yield scrapy.Request(twenty_comments_url,callback=self.parse_comment)

    def parse_comment(self,response):
        movie_comments = response.xpath('//span[@class="short"]/text()').extract()
        for movie_single_comment in movie_comments:
            print(movie_single_comment)