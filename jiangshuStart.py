from scrapy import cmdline

#爬取简书网中所有的内容，采取crawl spider
cmdline.execute(["scrapy","crawl","js_spider"])