FROM python:3.11.6

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y gcc

WORKDIR /usr/src/app

COPY reqs.txt /usr/src/app/reqs.txt

RUN pip install --upgrade pip && \
    pip install -r reqs.txt

COPY . /usr/src/app/
