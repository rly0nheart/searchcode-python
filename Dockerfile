FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip poetry \
    && poetry install \
    && apt-get clean

ENTRYPOINT ["searchcode"]