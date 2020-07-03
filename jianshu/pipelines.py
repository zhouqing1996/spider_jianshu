# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
# 连接池
from twisted.enterprise import adbapi
from pymysql import cursors


class JianshuPipeline(object):
    def __init__(self):
        dbparams = {
            'host': '120.78.150.89',
            'port': '3306',
            'user': 'root',
            'password': 'zhouqing',
            'database': 'spider',
            'charset': 'utf8'
        }
        # self.connect = pymysql.connect(**dbparams)
        self.connect = pymysql.connect(host='120.78.150.89', port=3306, user='root', password='zhouqing', db='spider',
                                       charset='utf8')
        # 游标
        self.cursor = self.connect.cursor()
        self._sql = None
        pass

    def process_item(self, item, spider):
        title = item['title']
        content = item['content']
        author = item['author']
        avatar = item['avatar']
        pub_time = item['pub_time']
        origin_url = item['origin_url']
        article_id = item['article_id']
        self.cursor = self.connect.cursor()
        self.cursor.execute('select count(*) from `jianshu_article`')
        count = self.cursor.fetchone()
        # self.cursor.execute(self.sql, (count,title, content, author, avatar, pub_time, origin_url, article_id))
        self.cursor.execute('insert into `jianshu_article` values(%s,%s,%s,%s,%s,%s,%s,%s)',
                            (count, title, content, author, pub_time, article_id, origin_url, avatar))
        self.connect.commit()
        return item

    @property
    def sql(self):
        if not self._sql:
            self._sql = 'insert into `jianshu_article`values(%s,%s,%s,%s,%s,%s,%s,%s)'
            # self._sql = """
            # insert into jianshu_article(id,title,content,author,avatar,pub_time,origin_url,article_id) values(null,%s,%s,%s,%s,%s,%s,%s)
            # """
            return self._sql
        return self._sql
        pass


# 利用连接池实现数据库存储
class JianshuPoolPipeline(object):
    def __init__(self):
        # 连接数据库池
        self.dbpool = adbapi.ConnectionPool('pymysql', host='120.78.150.89', port=3306, user='root',
                                            password='zhouqing', db='spider',
                                            charset='utf8')
        pass

    def process_item(self, item, spider):
        defer = self.dbpool.runInteraction(self.insert_item, item)
        defer.addErrback(self.handle_error, item, spider)
        pass

    # 插入
    def insert_item(self, cursor, item):
        title = item['title']
        content = item['content']
        author = item['author']
        avatar = item['avatar']
        pub_time = item['pub_time']
        origin_url = item['origin_url']
        article_id = item['article_id']
        subject = item['subject']
        cursor.execute('select count(*) from `jianshu_article_1`')
        count = cursor.fetchone()
        cursor.execute('insert into `jianshu_article_1` values(%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                       (count, title, content, author, pub_time, article_id, origin_url, avatar,subject))
        pass

    # 处理错误
    def handle_error(self, error, item, spider):
        print("error:")
        print(error)
        pass
