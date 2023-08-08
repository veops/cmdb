### Install

- Start mysql, redis
- Create mysql database: cmdb
- Pull code

  ```bash
  git clone https://github.com/veops/cmdb.git
  cd cmdb
  cp cmdb-api/settings.example.py cmdb-api/settings.py
  ```

  **set database in config file cmdb-api/settings.py**

- Install library
  - backend: `cd cmdb-api && pipenv run pipenv install && cd ..`
  - frontend: `cd cmdb-ui && yarn install && cd ..`
- Suggest step: (default: user:demo,password:123456)
- Create tables of cmdb database:
  in **cmdb-api** directory: `pipenv run flask db-setup && pipenv run flask cmdb-init-cache`

  ` source docs/cmdb.sql`

- Start service

  - backend: in **cmdb-api** directory: `pipenv run flask run -h 0.0.0.0`
  - frontend: in **cmdb-ui** directory: `yarn run serve`
  - worker: 
    - in **cmdb-api** directory: `pipenv run celery -A celery_worker.celery worker -E -Q one_cmdb_async --concurrency=1 -D`
    - in **cmdb-api** directory: `pipenv run celery -A celery_worker.celery worker -E -Q acl_async --concurrency=1 -D`

  - homepage: [http://127.0.0.1:8000](http://127.0.0.1:8000)
    - if not run localhost: please change ip address(**VUE_APP_API_BASE_URL**) in config file **cmdb-ui/.env** into your backend ip address
