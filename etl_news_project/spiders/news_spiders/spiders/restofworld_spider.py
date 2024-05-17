import scrapy
from ..items import ArticleItem

class RestOfWorldSpider(scrapy.Spider):
    name = 'restofworld_spider'
    start_urls = ['https://restofworld.org/series/the-rise-of-ai/']

    def parse(self, response):
        for article in response.css('article'):
            item = ArticleItem()
            item['title'] = article.css('h1::text').get()
            item['url'] = response.urljoin(article.css('a::attr(href)').get())
            item['body'] = article.css('div.article-body').get()
            item['pub_datetime'] = article.css('time::attr(datetime)').get()
            item['author'] = article.css('span.author::text').get()
            item['images'] = article.css('img::attr(src)').getall()
            yield item
