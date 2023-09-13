from app.models.models import User
from app.utils import singleton
from app.repository.abstract_repository import AbstractRepository
from app.repository.news_repository import NewsRepository

@singleton
class UserRepository(AbstractRepository):

    def entity(self):
        return User

    def find_user_by_email(self, email):

        print(email, "=========================================================================")

        user = self.entity().query.filter_by(email=email).first()
        print(user, "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        return user

    def save_news_for_user(self, user_id, news_id):

        user = self.find_by_id(user_id)
        news = NewsRepository().find_by_id(news_id)
        user.news.append(news)

        return self.save(user)

    def get_save_news_for_user(self, user_id):

        saved_news = self.entity().query.filter(self.entity().users.any(user_id=user_id)).all()
        return saved_news
