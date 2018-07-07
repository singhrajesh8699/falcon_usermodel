# -*- coding: utf-8 -*-

#https://devhub.io/repos/antonizoon-falcon-rest-api

import os
import configparser
from itertools import chain

BRAND_NAME = 'Fortraiz admin Dashboard'

SECRET_KEY = 'xs4G5ZD9SwNME6nWRWrK_aq6Yb9H8VJpdwCzkTErFPw='
UUID_LEN = 10
UUID_ALPHABET = ''.join(map(chr, range(48, 58)))
TOKEN_EXPIRES = 3600

APP_ENV = os.environ.get('APP_ENV') or 'test'
INI_FILE = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        '../config/test.ini'.format(APP_ENV))

CONFIG = configparser.ConfigParser()
CONFIG.read(INI_FILE)
MYSQL = CONFIG['mysql']


if APP_ENV == 'production' or APP_ENV == 'test':
    DB_CONFIG = (MYSQL['user'], MYSQL['password'], MYSQL['host'], MYSQL['database'])
    DATABASE_URL = "mysql://%s:%s@%s/%s" % DB_CONFIG


DB_ECHO = True if CONFIG['database']['echo'] == 'yes' else False
DB_AUTOCOMMIT = True

LOG_LEVEL = CONFIG['logging']['level']
