FROM python:3.8-slim

RUN apt-get update && apt-get install -y libpq-dev gcc

COPY requirements.txt /tmp/requirements.txt
COPY requirements-dev.txt tmp/requirements-dev.txt
RUN pip install -r /tmp/requirements.txt
RUN pip install -r /tmp/requirements-dev.txt
RUN apt-get autoremove -y gcc

EXPOSE 5000

COPY . /var/www/app
WORKDIR /var/www/app
