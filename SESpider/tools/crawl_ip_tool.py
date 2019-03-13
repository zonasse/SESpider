import pymysql
from SESpider.settings import USER_AGENT
import requests
from scrapy.selector import Selector
db_connect = pymysql.connect('localhost','root','ppz7long','SESpider')
cursor = db_connect.cursor()

create_table_sql = """
    CREATE TABLE IF NOT EXISTS t_IP (
        id INTEGER AUTO_INCREMENT PRIMARY KEY,
        ip VARCHAR(16),
        port INTEGER ,
        type VARCHAR(32)
    )
"""

cursor.execute(create_table_sql)


def crawl_ip_list():
    headers = {'User-Agent':USER_AGENT}
    for i in range(1,10):
        response = requests.get(url='https://www.xicidaili.com/nn/{}'.format(i),headers=headers)
        selector = Selector(text=response.text)
        all_trs = selector.xpath('//table[@id="ip_list"]/tr')

        for tr in all_trs[1:]:

            ip = tr.xpath('td/text()').extract()[0]
            port = tr.xpath('td/text()').extract()[1]
            type = tr.xpath('td/text()').extract()[5]
            # address = tr.xpath('td/a/text()').extract()
            insert_sql = """
                INSERT INTO t_IP (ip,port,type) VALUES ('{0}','{1}','{2}')
            """.format(ip,port,type)
            print(insert_sql)
            try:
                cursor.execute(insert_sql)
                db_connect.commit()
            except Exception as e:
                db_connect.rollback()


class crawl_ip_tool():
    def get_random_ip(self):
        query_sql = """
            SELECT ip,port,type FROM t_IP ORDER BY RAND() LIMIT 1
        """
        cursor.execute(query_sql)
        for ip_info in cursor.fetchall():
            ip = ip_info[0]
            port = ip_info[1]
            type = ip_info[2]
            if self.judge_ip_is_valid(ip,port,type):
                return 'http://{0}:{1}'.format(ip,port)
            else:
                return self.get_random_ip()


    def delete_ip(self,ip):
        delete_sql = """
                    DELETE FROM t_IP WHERE ip='{0}'
                """.format(ip)
        try:
            cursor.execute(delete_sql)
            db_connect.commit()
        except Exception as e:
            print(e)
            db_connect.rollback()

    def judge_ip_is_valid(self,ip,port,type):
        test_url = 'https://www.baidu.com/'
        proxy_url = 'http://{0}:{1}'.format(ip,port)
        try:
            proxy_dict = {
                "http":proxy_url
            }
            response = requests.get(test_url,proxies=proxy_dict)
        except Exception as e:
            self.delete_ip(ip)
            print('link failed')
            return False
        else:
            status_code = response.status_code
            if  status_code >= 200 and status_code < 300:
                print('link succeed')
                return True
            else:
                self.delete_ip(ip)
                return False

if __name__ == '__main__':
    # crawl_ip_list()
    ip_tool = crawl_ip_tool()
    print(ip_tool.get_random_ip())