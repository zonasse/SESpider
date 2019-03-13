# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose,TakeFirst
from SESpider.models.elasticsearchModels import *
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Search,Q
from elasticsearch import Elasticsearch

elastic = connections.create_connection(DoubanMovieType._doc_type.using)


class DoubanMovieItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class DoubanMovieItem(scrapy.Item):
    movie_directors = scrapy.Field()
    # movie_rate = scrapy.Field()
    # movie_star = scrapy.Field()
    movie_title = scrapy.Field()
    movie_url = scrapy.Field()
    movie_casts = scrapy.Field()
    movie_cover = scrapy.Field()
    movie_id = scrapy.Field()
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
            doubanMovieType = DoubanMovieType.get(id=int(self['movie_id']))
        except Exception as e:
            print('has except')
            doubanMovieType = DoubanMovieType(meta={'id':int(self['movie_id'])})
        doubanMovieType.movie_directors = self['movie_directors']
        # doubanMovieType.movie_rate = self['movie_rate']
        # doubanMovieType.movie_star = self['movie_star']
        doubanMovieType.movie_title = self['movie_title']
        doubanMovieType.movie_url = self['movie_url']
        doubanMovieType.movie_casts = self['movie_casts']
        doubanMovieType.movie_cover = self['movie_cover']
        doubanMovieType.movie_id = self['movie_id']
        doubanMovieType.movie_abstract = self['movie_abstract']
        doubanMovieType.suggest = gen_suggests(DoubanMovieType._doc_type.index, ((doubanMovieType.movie_title,10),(doubanMovieType.movie_abstract, 7)))

        doubanMovieType.save()


        return

def gen_suggests(index, info_tuple):
    # 根据字符串生成搜索建议数组
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

if __name__ == '__main__':

    # elastic = Elasticsearch('localhost:9200')
    elastic = connections.create_connection(DoubanMovieType._doc_type.using)

    query = {"query":{"match":{
        "movie_id":"1291999"
    }}}

    res = elastic.search(body=query)
    if res:
        print("record exists")

