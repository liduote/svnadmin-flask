import os
import subprocess

import pymysql

from config import Config

conn = pymysql.connect(host=Config.MYSQL_HOST,
                       port=int(Config.MYSQL_PORT),
                       user=Config.MYSQL_USER,
                       password=Config.MYSQL_PASS,
                       database=Config.MYSQL_DB,
                       charset='utf8')

cur = conn.cursor()

try:
    os.chdir('/svnadmin-flask')
    os.environ.setdefault('FLASK_APP', 'manage.py')
    status, output = subprocess.getstatusoutput('flask db upgrade')
    print(status)
    print(output)
except Exception as e:
    raise e
finally:
    conn.close()  # 关闭连接
