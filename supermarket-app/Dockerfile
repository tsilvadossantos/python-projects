FROM ubuntu:latest

MAINTAINER Thiago dos Santos

RUN apt-get update -y && apt-get install -y python-pip python-dev build-essential

ADD requirements.txt /usr/local/bin/

RUN pip install setuptools && pip install -r /usr/local/bin/requirements.txt

ENV BASE_DIR=/srv

ENV APP_DIR=$BASE_DIR/application/src/core

ADD ./src/core $APP_DIR

VOLUME $APP_DIR
