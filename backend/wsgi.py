from app import app
from app.routes.users_rest_api import user_api
from app.routes.news_rest_api import news_api

if __name__ == "__main__":

    app.register_blueprint(user_api)

    app.register_blueprint(news_api)

    app.run()