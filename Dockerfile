FROM python:3.11-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

COPY ./requirements.txt /requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY app /usr/src/app/
COPY entrypoint.sh /usr/src/app

EXPOSE 8000

RUN adduser -D myuser
USER myuser

ENTRYPOINT ["./entrypoint.sh"]
