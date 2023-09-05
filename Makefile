default: help
help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z0-9_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
.PHONY: help

env: ## Create a development environment using pipenv
	sudo easy_install pip && \
	pip install pipenv -i https://pypi.douban.com/simple && \
	npm install yarn && \
	make deps
.PHONY: env

docker-mysql: ## deploy MySQL use docker
	@docker run --name some-mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=my-secret-pw -d mysql:latest
.PHONY: docker-mysql

docker-redis: ## deploy Redis use docker
	@docker run --name some-redis -p 6379:6379 -d redis:latest
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
	cd cmdb-api && pipenv run celery -A celery_worker.celery worker -E -Q one_cmdb_async --concurrency=1 -D && pipenv run celery -A celery_worker.celery worker -E -Q acl_async --concurrency=1 -D
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
