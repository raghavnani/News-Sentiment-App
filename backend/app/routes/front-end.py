
from flask import Blueprint, render_template

frontend_api = Blueprint('front_end_api', __name__)
#


@frontend_api.route('/')
def hello_world():
    return render_template('index.html')