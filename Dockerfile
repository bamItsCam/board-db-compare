FROM python:2.7-alpine

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

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]