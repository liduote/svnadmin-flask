FROM rosslavery/git-node-alpine as nodebuilder

ENV web_src https://github.com/liduote/svnadmin-web.git

WORKDIR /

RUN git clone ${web_src} &&\
cd svnadmin-web && npm install && npm run build

FROM centos:7
RUN echo -e "[WandiscoSVN] \n\
name=Wandisco SVN Repo \n\
baseurl=http://opensource.wandisco.com/centos/7/svn-1.11/RPMS/x86_64/ \n\
enabled=1 \n\
gpgcheck=0" > /etc/yum.repos.d/svn.repo &&\
yum install -y epel-release &&\
yum install -y subversion httpd mod_dav_svn mod_ldap python3 python3-pip nginx mysql-devel

RUN groupadd svn -g 10399 && useradd svn -u 10399 -g svn

COPY --from=nodebuilder /svnadmin-web/dist /svnadmin-web/

COPY . /svnadmin-flask

RUN cp /svnadmin-flask/docker/entrypoint.sh /entrypoint.sh &&\
chmod a+x /entrypoint.sh && pip3 install -r /svnadmin-flask/requirements.txt

ENV LANG en_US.utf8

CMD /entrypoint.sh