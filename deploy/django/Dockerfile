FROM ubuntu:latest

WORKDIR /app

RUN apt-get update
# RUN apt-get install -y ca-certificates
# RUN mv /etc/apt/sources.list /etc/apt/sources.list.bak
# COPY ./_mirror_cn/tuna-sources.list /etc/apt/sources.list
RUN apt-get update
RUN apt-get install -y python3-pip mysql-client libmysqlclient-dev vim iputils-ping net-tools supervisor
COPY ./django/requirements.txt /app/requirements.txt
RUN python3 -m pip install --upgrade pip -i https://pypi.douban.com/simple
RUN python3 -m pip install -r /app/requirements.txt -i https://pypi.douban.com/simple

RUN mkdir static && mkdir appdata && chmod +777 -R appdata/

COPY ./django/production.sh /production.sh
RUN chmod +x /production.sh

COPY ./django/supervise.conf /etc/supervisor/conf.d/django.conf