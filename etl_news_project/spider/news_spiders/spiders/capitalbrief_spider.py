import scrapy
from ..items import ArticleItem

class CapitalBriefSpider(scrapy.Spider):
    name = 'capitalbrief_spider'
    start_urls = ['https://www.capitalbrief.com/technology/']

    def parse(self, response):
        for article in response.css('article'):
            item = ArticleItem()
            item['title'] = article.css('h2::text').get()
            item['url'] = response.urljoin(article.css('a::attr(href)').get())
            item['body'] = article.css('div.article-content').get()
            item['pub_datetime'] = article.css('time::attr(datetime)').get()
            item['author'] = article.css('span.author::text').get()
            item['images'] = article.css('img::attr(src)').getall()
            yield item
