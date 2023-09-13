import time
from app.models.models import News
from app.api_crawler.newsfilter_api import get_urls
from multiprocessing import Process, Queue, Manager
from app.repository.news_repository import NewsRepository
from app.services.abstract_service import AbstractService
from app.utils import singleton
import datetime
from app.utils import PreprocessInput
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

@singleton
class NewsService(AbstractService):

    def __init__(self):

        self.spiders = ["NewsFilter"]

        self.preprocessor = PreprocessInput()

        scheduler = BackgroundScheduler()
        scheduler.add_job(func=self.do_scrape_news_filter, trigger="interval", seconds=60)
        scheduler.start()
        atexit.register(lambda: scheduler.shutdown())


    def repository(self):
        return NewsRepository()

    def do_scrape_news_filter(self):
        print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))

        articles = get_urls()
        return_articles = []

        for article in reversed(articles):

            try:

                saved_news = self.repository().find_news_by_news_filter_id(article['news_filter_id'])

                print('=================================================================================', saved_news)

                if saved_news is None:
                    manager = Manager()
                    return_dict = manager.dict()
                    return_dict['article'] = article
                    q = Queue()
                    p = Process(target=self.preprocessor.run_crawler_in_loop, args=(q, return_dict))
                    p.start()
                    queue = q.get()
                    p.join()

                    if queue is not None:
                        raise queue

                    return_articles.append(self.save_news_article(return_dict['updated_article']))

            except Exception as e:
                print(e)

        results = return_articles

        return results

    def save_news_article(self, article):

        news = News(news_filter_id=article['news_filter_id'], source=article['source'], title=article['title'],
                    content=article['content'], description=article['description'], url=article['url'],
                    image_url=article['imageUrl'], published_at=str(datetime.datetime.now()).split('.')[0],
                    logits=article['logits'], sentiment=article['sentiment'], text=article['text'])

        return self.save(news)

    def get_news_with_condition(self, condition):

        if condition == 'Latest':
            return self.repository().get_latest_news()
        else:
            return self.repository().find_news_by_condition(condition)

    def get_save_news_for_user(self, user_id):
        return self.repository().get_save_news_for_user(user_id)

    def get_news_by_news_filter_id(self, news_filter_id):
        return self.repository().find_news_by_news_filter_id(news_filter_id)

    def get_latest_news(self):
        return self.repository().get_latest_news()