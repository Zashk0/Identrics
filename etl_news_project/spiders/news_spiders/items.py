import scrapy

class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    body = scrapy.Field()
    pub_datetime = scrapy.Field()
    author = scrapy.Field()
    images = scrapy.Field()
    ner = scrapy.Field()
    id = scrapy.Field()
