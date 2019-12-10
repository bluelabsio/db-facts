# syntax = docker/dockerfile:1.0-experimental

FROM python:3.7

WORKDIR /usr/src/app

COPY requirements.txt setup.py /usr/src/app/

RUN --mount=type=secret,id=pipconf,dst=/etc/pip.conf \
  pip3 install --no-cache-dir -r requirements.txt -e '/usr/src/app[movercli]'

COPY . /usr/src/app
