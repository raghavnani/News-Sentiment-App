import scrapy
from logging import log
from scrapy.crawler import CrawlerProcess


class NewsFilter(scrapy.Spider):

    name = "NewsFilter"
    start_urls = ['https://newsfilter.io/articles/']

    def __init__(self, url,**kwargs):
        # self.url = "https://newsfilter.io/articles/dish-network-corp-nasdaqdish-receives-consensus-rating-of-hold-from-brokerages-447168158f313be7f2b95626b0fc4522"
        self.url = url
        super().__init__(**kwargs)

    def parse(self, response):

            try:
                yield scrapy.Request(url=self.url, callback=self.extract)
            except:
                log("page skipped")

    def extract(self, response):

        row = {}

        array_p = response.css('article>p')

        if len(array_p) == 0:
            array_p = response.css('article>div>p')

        if len(array_p) == 0:
            array_p = response.css('article>div>div>p')

        text = ''

        for p in array_p:

            if not p.css('b'):
                text_list = p.css("::text").extract()

                for i in text_list:
                    if text == '':
                        text = i
                    elif text.endswith('\"') or text.endswith('\''):
                        text += '. ' + i
                    else:
                        text += ' ' + i
            else:
                break

        row['text'] = text

        # print(text)

        yield row


