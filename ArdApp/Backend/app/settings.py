import os
from dotenv import load_dotenv, find_dotenv
import uuid
import datetime

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
SECRET_KEY = os.environ.get('SECRET_KEY')