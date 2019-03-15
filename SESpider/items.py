# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import redis
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose,TakeFirst
from SESpider.models.elasticsearchModels import *
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Search,Q
from elasticsearch import Elasticsearch

elastic = connections.create_connection(MovieType._doc_type.using)
redis_cli = redis.StrictRedis()


# 根据字符串生成搜索建议数组
def generate_suggests(index, info_tuple):
    used_words = set()
    suggests = []
    for text, weight in info_tuple:
        if text:
            # 调用es的analyze接口分析字符串
            words = elastic.indices.analyze(index=index, analyzer="ik_max_word", params={'filter': ["lowercase"]},
                                       body=text)
            anylyzed_words = set([r["token"] for r in words["tokens"] if len(r["token"]) > 1])
            new_words = anylyzed_words - used_words
        else:
            new_words = set()

        if new_words:
            suggests.append({"input": list(new_words), "weight": weight})

    return suggests

class MovieItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class DoubanMovieItem(scrapy.Item):
    #id
    movie_id = scrapy.Field()
    #导演
    movie_directors = scrapy.Field()
    #评分
    movie_rate = scrapy.Field()
    #标题
    movie_title = scrapy.Field()
    #url
    movie_url = scrapy.Field()
    #演员
    movie_casts = scrapy.Field()
    #封面
    movie_cover = scrapy.Field()
    #简介
    movie_abstract = scrapy.Field()

    def save_to_es(self):
        # query = {"query": {"match": {
        #     "movie_id": self['movie_id']
        # }}}
        # # elastic.update(body=)
        # res = elastic.search(body=query)
        # if res:
        #     print('exists')
        try:
            movieType = MovieType.get(id=self['movie_id'])
        except Exception as e:
            print('has except')
            movieType = MovieType(meta={'id':self['movie_id']})
        movieType.movie_directors = self['movie_directors']
        movieType.movie_rate = self['movie_rate']
        movieType.movie_title = self['movie_title']
        movieType.movie_url = self['movie_url']
        movieType.movie_casts = self['movie_casts']
        movieType.movie_cover = self['movie_cover']
        movieType.movie_id = self['movie_id']
        movieType.movie_abstract = self['movie_abstract']
        movieType.suggest = generate_suggests(MovieType._doc_type.index, ((movieType.movie_title,10),(movieType.movie_abstract, 7)))
        movieType.movie_download_url = ''
        movieType.save()
        redis_cli.incr("douban_movie_count")
        return

class DyttMovieItem(scrapy.Item):
    #id
    movie_id = scrapy.Field()
    #导演
    movie_directors = scrapy.Field()
    #评分
    movie_rate = scrapy.Field()
    #标题
    movie_title = scrapy.Field()
    #url
    movie_url = scrapy.Field()
    #演员
    movie_casts = scrapy.Field()
    #封面
    movie_cover = scrapy.Field()
    #简介
    movie_abstract = scrapy.Field()
    #下载链接
    movie_download_url = scrapy.Field()

    def save_to_es(self):
        try:
            movieType = MovieType.get(id=self['movie_id'])
        except Exception as e:
            print('has except')
            movieType = MovieType(meta={'id':self['movie_id']})
        movieType.movie_directors = ''
        movieType.movie_rate = ''
        movieType.movie_title = self['movie_title']
        movieType.movie_url = self['movie_url']
        movieType.movie_casts = ''
        movieType.movie_cover = self['movie_cover']
        movieType.movie_id = self['movie_id']
        movieType.movie_abstract = ''
        movieType.suggest = generate_suggests(MovieType._doc_type.index, ((movieType.movie_title,10),))
        movieType.movie_download_url = self['movie_download_url']
        movieType.save()
        redis_cli.incr("dytt_movie_count")
        return



if __name__ == '__main__':
    pass
    # elastic = Elasticsearch('localhost:9200')
    # elastic = connections.create_connection(DoubanMovieType._doc_type.using)
    #
    # query = {"query":{"match":{
    #     "movie_id":"1291999"
    # }}}
    #
    # res = elastic.search(body=query)
    # if res:
    #     print("record exists")

