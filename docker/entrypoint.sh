#!/bin/bash
set -e
# 创建目录
base_path=${BASE_DIR:-/data}
data_path=$base_path'/svn'
log_path=$base_path'/log' 
mkdir -p ${data_path}
mkdir -p ${log_path}

# 修改httpd的配置
sed -i 's@#ServerName www.example.com:80@ServerName www.example.com:88@' /etc/httpd/conf/httpd.conf
sed -i 's@User apache@User svn@' /etc/httpd/conf/httpd.conf
sed -i 's@Group apache@Group svn@' /etc/httpd/conf/httpd.conf
sed -i 's@Listen 80@Listen 88@' /etc/httpd/conf/httpd.conf

auth_type=${AUTH_TYPE:-mysql}
if [ "$auth_type" = "mysql" ]; then
  mysql_host=${MYSQL_HOST:-localhost}
  mysql_port=${MYSQL_PORT:-3306}
  mysql_db=${MYSQL_DB:svnadmin}
  mysql_user=${MYSQL_USER:svnadmin}
  mysql_pass=${MYSQL_PASS:password}
  mysql_table_name=${MYSQL_USER_TABLE_NAME:-user}
  mysql_username_field=${MYSQL_USER_FIELD_NAME:-username}
  mysql_password_field=${MYSQL_PASS_FIELD_NAME:-password}
  /bin/cp -rf /svnadmin-flask/docker/subversion_mysql.conf /etc/httpd/conf.d/subversion.conf
  sed -i 's@{DATA_DIR}@'${data_path}'@' /etc/httpd/conf.d/subversion.conf
  sed -i 's@{MYSQL_HOST}@'${mysql_host}'@' /etc/httpd/conf.d/subversion.conf
  sed -i 's@{MYSQL_PORT}@'${mysql_port}'@' /etc/httpd/conf.d/subversion.conf
  sed -i 's@{MYSQL_USER}@'${mysql_user}'@' /etc/httpd/conf.d/subversion.conf
  sed -i 's@{MYSQL_PASS}@'${mysql_pass}'@' /etc/httpd/conf.d/subversion.conf
  sed -i 's@{MYSQL_DB}@'${mysql_db}'@' /etc/httpd/conf.d/subversion.conf
  sed -i 's@{MYSQL_USER_TABLE_NAME}@'${mysql_table_name}'@' /etc/httpd/conf.d/subversion.conf
  sed -i 's@{MYSQL_USER_FIELD_NAME}@'${mysql_username_field}'@' /etc/httpd/conf.d/subversion.conf
  sed -i 's@{MYSQL_PASS_FIELD_NAME}@'${mysql_password_field}'@' /etc/httpd/conf.d/subversion.conf
elif [ "$auth_type" = "ldap" ]; then
  ldap_host=${LDAP_HOST:-ldap.example.com}
  ldap_port=${LDAP_PORT:-389}
  ldap_base=${LDAP_BASE}
  ldap_uid=${LDAP_UID:-cn}
  ldap_bind_dn=${LDAP_BIND_DN}
  ldap_pass=${LDAP_PASS}
  /bin/cp -rf /svnadmin-flask/docker/subversion.conf /etc/httpd/conf.d/subversion.conf
  sed -i 's@{DATA_DIR}@'${data_path}'@' /etc/httpd/conf.d/subversion.conf
  sed -i 's@{LDAP_HOST}@'${ldap_host}'@' /etc/httpd/conf.d/subversion.conf
  sed -i 's@{LDAP_PORT}@'${ldap_port}'@' /etc/httpd/conf.d/subversion.conf
  sed -i 's@{LDAP_BASE}@'${ldap_base}'@' /etc/httpd/conf.d/subversion.conf
  sed -i 's@{LDAP_UID}@'${ldap_uid}'@' /etc/httpd/conf.d/subversion.conf
  sed -i 's@{LDAP_BIND_DN}@'${ldap_bind_dn}'@' /etc/httpd/conf.d/subversion.conf
  sed -i 's@{LDAP_PASS}@'${ldap_pass}'@' /etc/httpd/conf.d/subversion.conf
else
  echo "AUTH_TYPE must be mysql or ldap"
  exit 1
fi

# 修改nginx配置
/bin/cp -rf /svnadmin-flask/docker/nginx.conf /etc/nginx/nginx.conf
svn_domain=${SVN_DOMAIN:-svnadmin.example.com}
svn_port=${SVN_PORT:-80}
svn_host=$svn_domain$svn_port
sed -i 's@{Host}@'${svn_host}'@' /etc/nginx/nginx.conf

python /svnadmin_flask/migrate.py
# 启动所有服务
supervisord -c /svnadmin-flask/supervisor.conf