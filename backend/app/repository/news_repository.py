
from app.models.models import News
from app.utils import singleton
from app.repository.abstract_repository import AbstractRepository

@singleton
class NewsRepository(AbstractRepository):

    def entity(self):
        return News

    def find_news_by_news_filter_id(self, news_filter_id):
        news = self.entity().query.filter_by(news_filter_id=news_filter_id).first()
        return news

    def find_news_by_condition(self, condition):
        news = self.entity().query.filter_by(sentiment=condition).order_by(self.entity().id.desc()).all()
        return news

    def get_latest_news(self):
        news = self.find_all()
        return news


    # def get_save_news_for_user(self, user_id):
    #
    #     saved_news = self.entity().query.filter(self.entity().users.any(user_id=user_id)).all()
    #     return saved_news




