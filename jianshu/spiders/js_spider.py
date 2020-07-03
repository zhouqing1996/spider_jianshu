import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jianshu.items import JianshuItem


class JsSpiderSpider(CrawlSpider):
    name = 'js_spider'
    allowed_domains = ['jianshu.com']
    start_urls = ['http://www.jianshu.com/']

    rules = (
        # 简书的地址规律：https://www.jianshu.com/
        Rule(LinkExtractor(allow=r'.*/p/[0-9a-z]{12}.*'), callback='parse_detail', follow=True),
    )

    def parse_detail(self, response):
        title = response.xpath('//h1[@class="_1RuRku"]/text()').get()
        author = response.xpath('//span[@class="FxYr8x"]/a/text()').get()
        avatar = response.xpath('//div[@class="_2mYfmT"]/a/img/@src').get()
        pub_time = response.xpath('//div[@class="s-dsoj"]/time/text()').get()
        # id直接拿
        # https://www.jianshu.com/p/9713ff94c4a5
        article_url1 = response.url
        # 以问号切割
        article_url2 = article_url1.split("?")[0]
        article_id = article_url2.split('/')[-1]
        origin_url = response.url
        content = response.xpath('//article[@class="_2rhmJa"]').get()
        subject = response.xpath('//div[@class="_2Nttfz"]/a/span/text()').getall()
        # 此时为列表，在MySQL中不支持列表,以逗号分割
        subject = ",".join(subject)
        item = JianshuItem(
            title=title,
            content=content,
            article_id=article_id,
            origin_url=origin_url,
            author=author,
            avatar=avatar,
            pub_time=pub_time,
            subject=subject
        )
        yield item
        # item = {}
        # #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        # #item['name'] = response.xpath('//div[@id="name"]').get()
        # #item['description'] = response.xpath('//div[@id="description"]').get()
        # return item
