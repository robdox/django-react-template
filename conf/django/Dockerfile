FROM python:3.8-slim
LABEL Robert Wells <rwells@dvele.com>

# Python can write to stdout / no pyc files
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Building a base image with our requirements
RUN mkdir /app
WORKDIR /app

# Install the requirements
COPY conf/django/requirements.txt .
RUN pip install -r requirements.txt

COPY conf/django/docker-entrypoint.sh ..
ENTRYPOINT ["../docker-entrypoint.sh"]
