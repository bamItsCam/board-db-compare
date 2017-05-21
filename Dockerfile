FROM python:2.7-alpine

RUN apk update && \
    apk upgrade && \
        apk add git && \
        apk add postgresql postgresql-client postgresql-dev && \
        apk add nginx python-dev libxml2 libxml2-dev libxslt libxslt-dev && \
        apk add --update --no-cache openrc g++ gcc && \
        pip install lxml Django requests gunicorn

RUN cd /tmp/ && \
    git clone git://github.com/bamItsCam/board-db-compare.git && \
    cp -r /tmp/board-db-compare/sbc_compare /usr/bin/ && \
    cp /tmp/board-db-compare/sbc-nginx.conf /etc/nginx/nginx.conf && \
    rm -rf /tmp/board-db-compare && \
    sed -i 's/DEBUG = True/DEBUG = False/g' /usr/bin/sbc_compare/sbc_compare/settings.py

WORKDIR /usr/bin/sbc_compare

RUN python manage.py collectstatic --noinput && \
    python manage.py populate_db && \
    python manage.py makemigrations && \
    python manage.py migrate --run-syncdb

RUN mkdir -p /run/nginx

EXPOSE 8080 8000

CMD /bin/sh -c "/usr/sbin/nginx && gunicorn sbc_compare.wsgi -b 127.0.0.1:8000"
