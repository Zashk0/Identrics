import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from ..items import ArticleItem
from etl.transform_data import clean_html, extract_entities
from datetime import datetime

class CapitalBriefSpider(scrapy.Spider):
    name = 'capitalbrief_spider'
    start_urls = ['https://www.capitalbrief.com/technology/']
    article_count = 0
    max_articles = 20

    def __init__(self, *args, **kwargs):
        super(CapitalBriefSpider, self).__init__(*args, **kwargs)
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

        article_links = sel.css('h2 a::attr(href)').getall()
        self.logger.info(f"Found {len(article_links)} article links")

        for article_link in article_links:
            if self.article_count < self.max_articles:
                self.logger.info(f"Following article link: {article_link}")
                yield response.follow(article_link, self.parse_article)
            else:
                return

        next_page = sel.css('a.next::attr(href)').get()
        if next_page and self.article_count < self.max_articles:
            self.logger.info(f"Found next page link: {next_page}")
            yield scrapy.Request(next_page, self.parse)

    def parse_article(self, response):
        self.driver.get(response.url)
        self.logger.info(f"Scraping article URL: {response.url} with status {response.status}")

        # Get the page source and create a Selector object
        sel = Selector(text=self.driver.page_source)

        item = ArticleItem()

        item['title'] = sel.css('h1::text').get()
        item['url'] = response.url
        item['body'] = ' '.join(sel.css('div.article-content p::text').getall())

        pub_datetime_str = sel.css('time.published::attr(datetime)').get()
        if pub_datetime_str:
            try:
                item['pub_datetime'] = datetime.fromisoformat(pub_datetime_str)
            except ValueError:
                item['pub_datetime'] = None
        else:
            item['pub_datetime'] = None

        author_name = sel.css('span.author-name::text').get() or sel.css('a.author::text').get()
        if author_name:
            item['author'] = author_name.replace("\u00c2\u00a0\u00a0", " ").strip()
        else:
            item['author'] = None

        # Update image extraction logic
        item['images'] = sel.css('div.article-content img::attr(src)').getall()
        item['images'] += sel.css('figure img::attr(src)').getall()
        item['images'] += sel.css('img::attr(src)').getall()  # Capture any remaining images

        body_text = clean_html(item['body'])
        item['ner'] = extract_entities(body_text)
    
        self.logger.info(f"Scraped data: {item}")

        yield item

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
