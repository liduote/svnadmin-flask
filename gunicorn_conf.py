import os
# 绑定的ip已经端口号
port = os.environ.get('BIND_PORT') or 5000
bind = f'0.0.0.0:%s' % port
# 监听队列
backlog = 512
# gunicorn要切换到的目的工作目录
chdir = '/svnadmin-flask'
# 超时
timeout = 30
# 使用gevent模式，还可以使用sync 模式，默认的是sync模式
# worker_class = 'gevent'
# 进程数
workers = os.environ.get('WORKER_NUM') or 3
# 指定每个进程开启的线程数
threads = 2
# 日志级别，这个日志级别指的是错误日志的级别，而访问日志的级别无法设置
loglevel = os.environ.get('LOG_LEVEL') or 'debug'
# 设置gunicorn访问日志格式，错误日志无法设置
access_log_format = '%(t)s %(p)s %(h)s “%(r)s” %(s)s %(L)s %(b)s %(f)s” “%(a)s”'
# 访问日志文件
accesslog = "{LOG_DIR}/gunicorn_access.log"
# 错误日志文件
errorlog = "{LOG_DIR}/gunicorn_error.log"
