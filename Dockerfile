FROM python:2.7-alpine
RUN addgroup -S sbc && adduser -S -g sbc sbc

RUN apk update && \
    apk upgrade && \
        apk add git && \
        apk add postgresql postgresql-client postgresql-dev && \
        apk add nginx python-dev libxml2 libxml2-dev libxslt libxslt-dev && \
        apk add --update --no-cache g++ gcc && \
        pip install lxml Django requests gunicorn

RUN cd /tmp/ && \
    git clone git://github.com/bamItsCam/board-db-compare.git && \
    cp -r /tmp/board-db-compare/sbc_compare /usr/bin/ && \
        rm -rf /tmp/board-db-compare

WORKDIR /usr/bin/sbc_compare

RUN python manage.py populate_db && \
    python manage.py makemigrations && \
    python manage.py migrate

RUN chown -R sbc.sbc /usr/bin/sbc_compare
EXPOSE 8000

USER sbc

CMD /bin/sh -c "gunicorn sbc_compare.wsgi -b 0.0.0.0:8000"
