from app.models.models import User
from app.utils import singleton
from app.services.abstract_service import AbstractService
from app.repository.user_repository import UserRepository


@singleton
class UserService(AbstractService):

    def repository(self):
        return UserRepository()

    def create_user(self, email, user_name, password):
        u = User(username=user_name, email=email)
        u.set_password(password)
        return self.save(u)

    def update_user(self, id, password):
        user = self.find_by_id(id)
        user.set_password(password)
        return self.save(user)

    def find_user_by_id(self, id):
        return self.find_by_id(id)

    def find_all_users(self):
        return self.find_all()

    def find_user_by_email(self, email, password):

        user = self.repository().find_user_by_email(email)
        print(user.username , '====================================================================')
        if user:
            if user.check_password(password):
                print("hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiihhhh")
                return {'user_name':user.username}
        return None

    def save_news_for_user(self, user_id, news_id):
        return self.repository().save_news_for_user(user_id, news_id)

