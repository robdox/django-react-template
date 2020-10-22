FROM python:3.8-alpine3.10
LABEL Robert Wells <rwells@dvele.com>

# Python can write to stdout / no pyc files
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Building a base image with our requirements
RUN mkdir /app
WORKDIR /app
COPY conf/django/requirements.txt .

RUN apk add --no-cache --virtual .build-deps \
    build-base postgresql-dev libffi-dev \
    && pip install -r requirements.txt \
    && find /usr/local \
        \( -type d -a -name test -o -name tests \) \
        -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
        -exec rm -rf '{}' + \
    && runDeps="$( \
        scanelf --needed --nobanner --recursive /usr/local \
          | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
          | sort -u \
          | xargs -r apk info --installed \
          | sort -u \
    )" \
    && apk add --virtual .rundeps $runDeps \
    && apk del .build-deps \
    && apk add --no-cache bash

COPY conf/django/docker-entrypoint.sh ..
ENTRYPOINT ["../docker-entrypoint.sh"]
