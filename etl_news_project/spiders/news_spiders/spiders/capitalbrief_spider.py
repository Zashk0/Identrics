import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import json
import os

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
        self.items = []

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

        item = {
            'title': sel.css('h1::text').get().replace("\ud83d\udd75\ufe0f\ud83d\udd75\ufe0f", " "),
            'url': response.url,
            'body': ' '.join(sel.css('div.briefing content content-open p::text').getall()),
            'pub_datetime': None,
            'author': None,
            'images': [],
            'ner': {}
        }

        pub_datetime = sel.css('time::attr(datetime)').get()
        if pub_datetime:
            item['pub_datetime'] = datetime.fromisoformat(pub_datetime.replace("Z", "")).isoformat()

        author_name = sel.css('span.author-name::text').get() or sel.css('a.author::text').get()
        if author_name:
            item['author'] = author_name.replace("\u00c2\u00a0\u00a0", " ").strip()

        # Update image extraction logic
        item['images'] = sel.css('div.article-content img::attr(src)').getall()
        item['images'] += sel.css('figure img::attr(src)').getall()
        item['images'] += sel.css('img::attr(src)').getall()  # Capture any remaining images

        self.items.append(item)
        self.article_count += 1

        self.logger.info(f"Scraped data: {item}")

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
        # Save JSON file to the correct directory
        output_dir = os.path.join(os.path.dirname(__file__), '..', 'spiders')
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, 'raw_data_capitalbrief.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.items, f, ensure_ascii=False, indent=4)
