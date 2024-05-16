from scrapy import signals
import logging

class SimpleLoggingMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s

    def process_request(self, request, spider):
        # Log each request made by the spider
        logging.debug(f"Request made: {request.url}")
        return None

    def process_response(self, request, response, spider):
        # Log each response received by the spider
        logging.debug(f"Response received: {response.url}")
        return response

    def process_exception(self, request, exception, spider):
        # Log any exceptions that occur during the request
        logging.error(f"Exception occurred: {request.url} - {exception}")
        return None

    def spider_opened(self, spider):
        logging.info(f"Spider opened: {spider.name}")

    def spider_closed(self, spider):
        logging.info(f"Spider closed: {spider.name}")
