import os
from os.path import join
from os.path import dirname
from dotenv import load_dotenv


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


APPID = os.environ.get('appId')
DSN = os.environ.get('DATABASE_URL')
