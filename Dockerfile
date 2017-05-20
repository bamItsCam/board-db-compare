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

RUN python manage.py collectstatic --noinput && \
    python manage.py populate_db && \
    python manage.py makemigrations && \
    python manage.py migrate --run-syncdb

Run sed -i '/http {/a \ \ \ \ include /etc/nginx/sites-enabled/*;' /etc/nginx/nginx.conf && \
    mkdir /etc/nginx/sites-enabled && \
    mkdir /etc/nginx/sites-available && \
    mv /usr/bin/sbc_compare/sbc-nginx.conf /etc/nginx/sites-available && \
    ln -s /etc/nginx/sites-available/sbc-nginx.conf /etc/nginx/sites-enabled/sbc-nginx.conf && \
    service nginx restart

RUN chown -R sbc.sbc /usr/bin/sbc_compare
EXPOSE 80

USER sbc

CMD /bin/sh -c "gunicorn sbc_compare.wsgi -b 127.0.0.1:8001 --daemon"
