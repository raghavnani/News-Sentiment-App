import os
from dotenv import load_dotenv
# Statement for enabling the development environment
DEBUG = True

# Define .env
load_dotenv()
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_CONNECTION = os.getenv("POSTGRES_CONNECTION")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

# Define the database
SQLALCHEMY_DATABASE_URI = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_CONNECTION}:{POSTGRES_PORT}/dashboard'

