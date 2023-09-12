FROM python:3.10.5

RUN mkdir /telebot

WORKDIR /telebot

COPY enums /telebot/enums/
COPY src /telebot/src/
COPY requirements.txt /telebot/
COPY LICENSE /telebot/

RUN pip install -r requirements.txt

CMD [ "python", "src/main.py" ]