import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from ..items import ArticleItem
from etl.transform_data import clean_html, extract_entities
from datetime import datetime

class RestOfWorldSpider(scrapy.Spider):
    name = 'rest_of_world_spider'
    start_urls = ['https://restofworld.org/series/the-rise-of-ai/']
    article_count = 0
    max_articles = 20

    def __init__(self, *args, **kwargs):
        super(RestOfWorldSpider, self).__init__(*args, **kwargs)
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    def parse(self, response):
        self.driver.get(response.url)
        self.logger.info(f"Crawling URL: {response.url} with status {response.status}")

        # Scroll to load dynamic content
        self.scroll_to_load()

        # Get the page source and create a Selector object
        sel = Selector(text=self.driver.page_source)

        article_links = sel.css('a.grid-story__link.article-link::attr(href)').getall()
        article_links += sel.css('a.article-link::attr(href)').getall()
        
        self.logger.info(f"Found {len(article_links)} article links")

        for article_link in article_links:
            if self.article_count < self.max_articles:
                self.logger.info(f"Following article link: {article_link}")
                yield response.follow(article_link, self.parse_article)
            else:
                return

        next_page = sel.css('a.o-card__more::attr(href)').get()
        if not next_page:
            next_page = sel.css('a.pagination__next::attr(href)').get()

        if next_page and self.article_count < self.max_articles:
            self.logger.info(f"Found next page link: {next_page}")
            yield scrapy.Request(next_page, self.parse)

    def parse_article(self, response):
        self.driver.get(response.url)
        self.logger.info(f"Scraping article URL: {response.url} with status {response.status}")

        # Get the page source and create a Selector object
        sel = Selector(text=self.driver.page_source)

        item = ArticleItem()

        item['title'] = sel.css('h1.post-header__text__title::text').get() or \
                        sel.css('h1.grid-story__hed.headline::text').get() or \
                        sel.css('h2.article-info__title.headline::text').get()
        item['url'] = response.url
        item['body'] = ' '.join(sel.css('div.post-container p::text').getall())

        pub_datetime_str = sel.css('div.contrib-date time::attr(datetime)').get() or \
                           sel.css('div.post-subheader__meta-date time::attr(datetime)').get()
        if pub_datetime_str:
            try:
                item['pub_datetime'] = datetime.fromisoformat(pub_datetime_str)
            except ValueError:
                item['pub_datetime'] = None
        else:
            item['pub_datetime'] = None

        item['author'] = sel.css('h2.contrib-byline a::text').get() or \
                         sel.css('div.post-subheader__byline a::text').get() or \
                         sel.css('div.article-info__byline a::text').get()

        # Update image extraction logic
        item['images'] = sel.css('div.image_container img::attr(src)').getall()
        item['images'] += sel.css('li.gallery__image img::attr(src)').getall()
        item['images'] += sel.css('div.gallery__image img::attr(src)').getall()
        item['images'] += sel.css('img::attr(src)').getall()  # Capture any remaining images

        body_text = clean_html(item['body'])
        item['ner'] = extract_entities(body_text)
    
        self.logger.info(f"Scraped data: {item}")

        yield item
        related_links = response.css('a.recirc-story__image-wrapper::attr(href)').getall()
        self.logger.info(f"Found {len(related_links)} related article links at the bottom")
        for link in related_links:
            yield response.follow(link, self.parse_article)
        self.article_count += 1

    def scroll_to_load(self):
        # Scroll down to the bottom to load more content
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.driver.implicitly_wait(2)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def closed(self, reason):
        self.driver.quit()
