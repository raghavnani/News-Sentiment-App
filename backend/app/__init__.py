from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os
from flask_cors import CORS

config = os.environ.get("CONFIG_MODULE", "config.prod")

app = Flask(__name__)
app.config.from_object(config)
cors = CORS(app)

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.models.models import *
# from app.models.user import User

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()
db.session.commit()