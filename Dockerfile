FROM python:3-alpine

RUN apk add --no-cache build-base

WORKDIR /

COPY . .

RUN pip install python-dotenv discord.py

CMD [ "python", "./setup.py" ]