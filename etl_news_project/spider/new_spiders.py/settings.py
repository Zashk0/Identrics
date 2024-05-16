# Scrapy settings for news_spiders project
BOT_NAME = 'news_spiders'

SPIDER_MODULES = ['news_spiders.spiders']
NEWSPIDER_MODULE = 'news_spiders.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure item pipelines
ITEM_PIPELINES = {
    'news_spiders.pipelines.NewsSpidersPipeline': 300,
}
