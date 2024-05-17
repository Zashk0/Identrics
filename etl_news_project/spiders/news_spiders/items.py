import scrapy

class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    body = scrapy.Field()
    url = scrapy.Field()
    pub_datetime = scrapy.Field()
    author = scrapy.Field()
    images = scrapy.Field()
    comments = scrapy.Field()
