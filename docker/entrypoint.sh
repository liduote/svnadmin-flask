#!/bin/bash
set -e
# 创建目录
mkdir -p /var/log/svnadmin
mkdir -p ${DATA_DIR}
# 修改httpd的配置
sed -i 's@#ServerName www.example.com:80@ServerName www.example.com:88@' /etc/httpd/conf/httpd.conf
sed -i 's@User apache@User svn@' /etc/httpd/conf/httpd.conf
sed -i 's@Group apache@Group svn@' /etc/httpd/conf/httpd.conf
sed -i 's@Listen 80@Listen 88@' /etc/httpd/conf/httpd.conf
# 修改subversion配置
/bin/cp -rf /svnadmin-flask/docker/subversion.conf /etc/httpd/conf.d/subversion.conf
sed -i 's@{DATA_DIR}@'${DATA_DIR}'@' /etc/httpd/conf.d/subversion.conf
sed -i 's@{LDAP_HOST}@'${LDAP_HOST}'@' /etc/httpd/conf.d/subversion.conf
sed -i 's@{LDAP_PORT}@'${LDAP_PORT}'@' /etc/httpd/conf.d/subversion.conf
sed -i 's@{LDAP_BASE}@'${LDAP_BASE}'@' /etc/httpd/conf.d/subversion.conf
sed -i 's@{LDAP_UID}@'${LDAP_UID}'@' /etc/httpd/conf.d/subversion.conf
sed -i 's@{LDAP_BIND_DN}@'${LDAP_BIND_DN}'@' /etc/httpd/conf.d/subversion.conf
sed -i 's@{LDAP_PASS}@'${LDAP_PASS}'@' /etc/httpd/conf.d/subversion.conf

# 修改nginx配置
/bin/cp -rf /svnadmin-flask/docker/nginx.conf /etc/nginx/nginx.conf

# 启动所有服务
supervisord -c /svnadmin-flask/supervisor.conf