FROM python:3.11-slim

RUN mkdir code
WORKDIR code

ADD . /code/
ADD .env.docker /code/.env

ENV APP_NAME=STEKLO_IDEA

RUN pip install -r requirements.txt
#RUN ./manage.py loaddata ./products.json

CMD gunicorn storeStekloIdea.wsgi:application -b 0.0.0.0:8000