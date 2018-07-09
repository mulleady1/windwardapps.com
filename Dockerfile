FROM python:3

LABEL Name=windwardapps Version=1.0.0

RUN mkdir /app
RUN mkdir /logs
WORKDIR /app/project
ADD . /app

RUN pip install --no-cache-dir -r ../requirements.txt
