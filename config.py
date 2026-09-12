# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# load example/.env by default if exists
load_dotenv(os.path.join(BASE_DIR, 'example', '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'change-this-secret')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///example/db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
