FROM python:3.12

RUN mkdir /bot

WORKDIR /bot

COPY requirements.txt .

RUN touch NSD.txt

RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "telegram_bot.py" ]

