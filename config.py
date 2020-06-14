import os


class Config:
    DEBUG = os.environ.get('DEBUG') or False
    SECRET_KEY = os.environ.get('SECRET_KEY') or \
        b'\x99\xfe(\x07\xb3\xc8H]7\xccYr\xd3K\xa3\x8b_\x04\x18\xcd\x9fYh\xa3'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
        'mysql+pymysql://' \
        'svnadmin_uo:20kTQFBS@devops-ingress.asiainfo.com:35676/svnadmin?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_POOL_RECYCLE = 3
    SQLALCHEMY_POOL_SIZE = 20

