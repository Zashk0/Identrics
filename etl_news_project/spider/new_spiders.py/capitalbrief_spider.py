import scrapy

class CapitalBriefSpider(scrapy.Spider):
    name = 'capitalbrief_spider'
    start_urls = ['https://www.capitalbrief.com/technology/']

    def parse(self, response):
        for article in response.css('article'):
            yield {
                'title': article.css('h1::text').get(),
                'url': response.urljoin(article.css('a::attr(href)').get()),
                'body': article.css('div.article-body').get(),
                'pub_datetime': article.css('time::attr(datetime)').get(),
                'author': article.css('span.author::text').get(),
                'images': article.css('img::attr(src)').getall(),
            }