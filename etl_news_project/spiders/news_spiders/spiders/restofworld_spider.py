import scrapy
from ..items import ArticleItem
from etl.transform_data import clean_html, extract_entities

class RestOfWorldSpider(scrapy.Spider):
    name = 'restofworld_spider'
    start_urls = ['https://restofworld.org/series/the-rise-of-ai/']
    article_count = 0
    max_articles = 20

    def parse(self, response):
        self.logger.info(f"Crawling URL: {response.url} with status {response.status}")

        # Check for different structures of article links
        article_links = response.css('a.grid-story__link.article-link::attr(href)').getall()
        article_links += response.css('a.article-link::attr(href)').getall()
        
        self.logger.info(f"Found {len(article_links)} article links")

        for article_link in article_links:
            if self.article_count < self.max_articles:
                self.logger.info(f"Following article link: {article_link}")
                yield response.follow(article_link, self.parse_article)
            else:
                return

        # Follow pagination links
        next_page = response.css('a.o-card__more::attr(href)').get()
        if not next_page:
            next_page = response.css('a.pagination__next::attr(href)').get()

        if next_page and self.article_count < self.max_articles:
            self.logger.info(f"Found next page link: {next_page}")
            yield response.follow(next_page, self.parse)

    def parse_article(self, response):
        self.logger.info(f"Scraping article URL: {response.url} with status {response.status}")

        item = ArticleItem()

        item['title'] = response.css('h1.post-header__text__title::text').get() or \
                        response.css('h1.grid-story__hed.headline::text').get() or \
                        response.css('h2.article-info__title.headline::text').get()
        item['url'] = response.url
        item['body'] = ' '.join(response.css('div.post-container p::text').getall())
        item['pub_datetime'] = response.css('div.contrib-date time::attr(datetime)').get() or \
                               response.css('div.post-subheader__meta-date time::attr(datetime)').get()
        item['author'] = response.css('h2.contrib-byline a::text').get() or \
                         response.css('div.post-subheader__byline a::text').get() or \
                         response.css('div.article-info__byline a::text').get()
        item['images'] = response.css('div.image_container img::attr(src)').getall()

        # Extract NER data and add to item
        body_text = clean_html(item['body'])
        item['ner'] = extract_entities(body_text)
    
        self.logger.info(f"Scraped data: {item}")

        yield item

        self.article_count += 1
