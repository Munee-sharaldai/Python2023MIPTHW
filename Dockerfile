FROM python:3

RUN apt update
RUN apt install python3 -y

WORKDIR /usr/app/src

COPY main.py ./
COPY database.py ./
COPY bot.py ./
COPY parse.py ./

RUN pip install selenium
RUN pip install webdriver-manager
RUN pip install pyTelegramBotAPI

CMD ["python", "main.py"]