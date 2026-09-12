# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# load .env from project root or instance/ if present. DO NOT load example/.env
# This allows SECRET_KEY to come from environment or from a local .env file only.
if os.path.exists(os.path.join(BASE_DIR, '.env')):
    load_dotenv(os.path.join(BASE_DIR, '.env'))
elif os.path.exists(os.path.join(BASE_DIR, 'instance', '.env')):
    load_dotenv(os.path.join(BASE_DIR, 'instance', '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'change-this-secret')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///example/db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
