MYSQL_ROOT_PASSWORD ?= root
MYSQL_PORT ?= 3306
REDIS_PORT ?= 6379

default: help
help:  ## display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z0-9_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
.PHONY: help

env: ## create a development environment using pipenv
	sudo easy_install pip && \
	pip install pipenv -i https://repo.huaweicloud.com/repository/pypi/simple && \
	npm install yarn && \
	make deps
.PHONY: env

docker-mysql: ## deploy MySQL use docker
	@docker run --name mysql -p ${MYSQL_PORT}:3306 -e MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD} -d mysql:latest
.PHONY: docker-mysql

docker-redis: ## deploy Redis use docker
	@docker run --name redis -p ${REDIS_PORT}:6379 -d redis:latest
.PHONY: docker-redis

deps: ## install dependencies using pip
	cd cmdb-api && \
	pipenv install --dev && \
	pipenv run flask db-setup && \
	pipenv run flask cmdb-init-cache && \
	cd .. && \
    cd cmdb-ui && yarn install && cd ..
.PHONY: deps

api: ## start api server
	cd cmdb-api && pipenv run flask run -h 0.0.0.0
.PHONY: api

worker: ## start async tasks worker
	cd cmdb-api && pipenv run celery -A celery_worker.celery worker -E -Q one_cmdb_async --autoscale=5,2 --logfile=one_cmdb_async.log -D && pipenv run celery -A celery_worker.celery worker -E -Q acl_async --autoscale=2,1 --logfile=one_acl_async.log -D
.PHONY: worker

ui: ## start ui server
	cd cmdb-ui && yarn run serve
.PHONY: ui

clean: ## remove unwanted files like .pyc's
	pipenv run flask clean
.PHONY: clean

lint: ## check style with flake8
	flake8 --exclude=env .
.PHONY: lint
