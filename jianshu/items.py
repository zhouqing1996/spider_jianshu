# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleItem(scrapy.Item):

    pass


class JianshuItem(scrapy.Item):
    title = scrapy.Field()  # 标题
    content = scrapy.Field()  # 内容
    article_id = scrapy.Field()  # 文件id
    origin_url = scrapy.Field()  # 原始url
    author = scrapy.Field()  # 作者
    avatar = scrapy.Field()  # 头像
    pub_time = scrapy.Field()  # 发布时间
    subject = scrapy.Field()  # 文章归纳
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
