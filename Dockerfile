FROM ubuntu:22.04
RUN apt-get update -y
RUN apt-get install -y python3-pip python-dev-is-python3 build-essential
RUN pip install --upgrade pip
RUN mkdir ./app
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["telegram_bot.py"]