from app import app
from app.routes.users_rest_api import user_api
from app.routes.news_rest_api import news_api
from flask import Flask, render_template

from flask import Flask
# app = Flask(__name__)



if __name__ == '__main__':


    app.register_blueprint(user_api)

    app.register_blueprint(news_api)

    # Run the application
    app.run(host="0.0.0.0", debug=True, port=5001)

