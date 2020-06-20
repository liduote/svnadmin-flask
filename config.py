import os


class Config:
    DEBUG = os.environ.get('DEBUG') or False
    SECRET_KEY = os.environ.get('SECRET_KEY') or \
        b'\x99\xfe(\x07\xb3\xc8H]7\xccYr\xd3K\xa3\x8b_\x04\x18\xcd\x9fYh\xa3'
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'localhost'
    MYSQL_PORT = os.environ.get('MYSQL_PORT') or 3306
    MYSQL_DB = os.environ.get('MYSQL_DB') or 'svnadmin'
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'svnadmin'
    MYSQL_PASS = os.environ.get('MYSQL_PASS') or 'password'

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'\
        .format(MYSQL_USER, MYSQL_PASS, MYSQL_HOST, MYSQL_PORT, MYSQL_DB)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    SQLALCHEMY_POOL_RECYCLE = 3
    SQLALCHEMY_POOL_SIZE = 20

    BASE_DIR = os.environ.get('BASE_DIR') or '/data'
    DATA_DIR = BASE_DIR + '/svn'

    HTTP_SCHEMA = 'https' if os.environ.get('HTTPS_ENABLE') == 'true' else 'http'
    SVN_DOMAIN = os.environ.get('SVN_DOMAIN') or 'svnadmin.example.com'
    SVN_PORT = os.environ.get('SVN_PORT')
    if not SVN_PORT or SVN_PORT == '80':
        SVN_BASE_URL = '{}://{}/svn'.format(HTTP_SCHEMA, SVN_DOMAIN)
    else:
        SVN_BASE_URL = '{}://{}:{}/svn'.format(HTTP_SCHEMA, SVN_DOMAIN, SVN_PORT)
