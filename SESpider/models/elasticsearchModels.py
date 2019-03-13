from elasticsearch_dsl import DocType, Completion,Keyword, Text, Integer, Boolean, Nested
from elasticsearch_dsl.analysis import CustomAnalyzer
from elasticsearch_dsl.connections import connections

connections.create_connection(hosts=['localhost'])

class CustomAnalyzer(CustomAnalyzer):
    def get_analysis_definition(self):
        return {}

ik_analyzer = CustomAnalyzer('ik_max_word', filter=['lowercase'])

class DoubanMovieType(DocType):
    suggest = Completion(analyzer = ik_analyzer)
    movie_id = Keyword()
    movie_directors = Text(analyzer = 'ik_max_word')
    # movie_rate = Keyword()
    # movie_star = Keyword()
    movie_title = Text(analyzer = 'ik_max_word')
    movie_url = Keyword()
    movie_casts = Text(analyzer = 'ik_max_word')
    movie_cover = Keyword()
    movie_abstract = Text(analyzer = 'ik_max_word')

    class Meta:
        index = 'douban'
        doc_type = 'movie'

# DoubanMovieType.init()