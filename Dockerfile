FROM ubuntu:latest

COPY . /app

WORKDIR /app

VOLUME ./:/app

RUN apt-get update \
  && apt-get install -y python3

RUN apt install -y python3-pip

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

RUN python3 manage.py makemigrations && python3 manage.py migrate