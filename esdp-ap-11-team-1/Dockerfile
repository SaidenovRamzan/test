FROM python:3.11.6

RUN apt-get update && apt-get install -y gcc

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY rentbooks/reqs.txt .

RUN python3 -m venv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r reqs.txt

COPY . .
