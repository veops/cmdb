.PHONY: env clean api ui worker

help:
	@echo "  env         create a development environment using pipenv"
	@echo "  deps        install dependencies using pip"
	@echo "  clean       remove unwanted files like .pyc's"
	@echo "  lint        check style with flake8"
	@echo "  api         start api server"
	@echo "  ui          start ui  server"
	@echo "  worker      start async tasks worker"

env:
	sudo easy_install pip && \
	pip install pipenv -i https://pypi.douban.com/simple && \
	npm install yarn && \
	make deps

deps:
	pipenv install --dev && \
	pipenv run flask db-setup && \
	pipenv run flask cmdb-init-cache && \
    cd cmdb-ui && yarn install && cd ..

api:
	cd cmdb-api && pipenv run flask run -h 0.0.0.0

worker:
	cd cmdb-api && pipenv run celery -A celery_worker.celery worker -E -Q one_cmdb_async --concurrency=1 -D && pipenv run celery -A celery_worker.celery worker -E -Q acl_async --concurrency=1 -D

ui:
	cd cmdb-ui && yarn run serve

clean:
	pipenv run flask clean

lint:
	flake8 --exclude=env .
