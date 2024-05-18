import scrapy
from ..items import ArticleItem

class CapitalBriefSpider(scrapy.Spider):
    name = 'capitalbrief_spider'
    start_urls = ['https://www.capitalbrief.com/technology/']

    def parse(self, response):
        # Add debug statement to log the response URL
        self.logger.info(f"Crawling URL: {response.url}")

        for article_link in response.css('article.post h2.entry-title a::attr(href)').getall():
            self.logger.info(f"Found article link: {article_link}")  # Debug statement
            yield response.follow(article_link, self.parse_article)

        next_page = response.css('a.next.page-numbers::attr(href)').get()
        if next_page:
            self.logger.info(f"Found next page link: {next_page}")  # Debug statement
            yield response.follow(next_page, self.parse)

    def parse_article(self, response):
        # Add debug statement to log the response URL
        self.logger.info(f"Scraping article URL: {response.url}")

        item = ArticleItem()
        item['title'] = response.css('h1.post-header__text__title::text').get()
        item['url'] = response.url
        item['body'] = ' '.join(response.css('div.entry-content p::text').getall())
        item['pub_datetime'] = response.css('time.entry-date::attr(datetime)').get()
        item['author'] = response.css('span.author a::text').get()
        item['images'] = response.css('img::attr(src)').getall()

        self.logger.info(f"Scraped data: {item}")  # Debug statement
        yield item
