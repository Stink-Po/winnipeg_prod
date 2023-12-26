FROM python:3.11-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /requirements.txt

RUN apk add --update --no-cache --virtual .tmp gcc
RUN apk add --update --no-cache libc-dev linux-headers
RUN apk update && apk upgrade
RUN pip install -r /requirements.txt
RUN apk del .tmp
RUN mkdir /app

COPY ./app /app
WORKDIR /app
COPY entrypoint.sh /scripts

RUN chmod +x /scripts/*



RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
RUN mkdir -p /vol/web/staticfiles

RUN adduser -D user
RUN chown -R user:user /vol
RUN chmod -R 755 /vol/web
USER user
CMD ["entrypoint.sh"]
