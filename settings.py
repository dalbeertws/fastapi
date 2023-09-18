import os
from dotenv import load_dotenv

load_dotenv()


DATABASE_NAME = os.environ.get('DATABASE_NAME')
DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
DATABASE_HOSTNAME = os.environ.get('DATABASE_HOSTNAME')
DATABASE_USER = os.environ.get('DATABASE_USER')


if not DATABASE_NAME or not DATABASE_NAME or not DATABASE_HOSTNAME or not DATABASE_USER:
    raise EnvironmentError("DATABASE creds are missing. Please check your .env file")


SECRET_KEY = os.environ.get('SECRET_KEY')


if SECRET_KEY is None:
    raise EnvironmentError("SECRET_KEY environment variable is missing")
