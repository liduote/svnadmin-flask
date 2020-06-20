import subprocess

import pymysql

from config import Config

conn = pymysql.connect(host=Config.MYSQL_HOST,
                       port=Config.MYSQL_PORT,
                       user=Config.MYSQL_USER,
                       password=Config.MYSQL_PASS,
                       database=Config.MYSQL_DB,
                       charset='utf8')

cur = conn.cursor()

sql = 'show tables;'
try:
    cur.execute(sql)  # 执行sql语句

    results = cur.fetchall()  # 获取查询的所有记录
    if not results:
        status, output = subprocess.getstatusoutput('flask db upgrade')
        print(status)
        print(output)
except Exception as e:
    raise e
finally:
    conn.close()  # 关闭连接
