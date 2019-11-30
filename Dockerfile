# ================================= UI ================================
FROM node:alpine AS builder

LABEL description="cmdb-ui"

COPY ui /data/apps/cmdb-ui

WORKDIR /data/apps/cmdb-ui

RUN sed -i "s#http://127.0.0.1:5000##g" .env && yarn install  && yarn build


FROM nginx:alpine AS cmdb-ui

RUN mkdir /etc/nginx/html && rm -f /etc/nginx/conf.d/default.conf

COPY --from=builder /data/apps/cmdb-ui/dist /etc/nginx/html/


# ================================= API ================================
FROM python:3.7-alpine AS cmdb-api

LABEL description="Python3.7,cmdb"

COPY . /data/apps/cmdb

WORKDIR /data/apps/cmdb

RUN apk add --no-cache tzdata gcc musl-dev libffi-dev

ENV TZ=Asia/Shanghai

RUN pip install  --no-cache-dir -r docs/requirements.txt \
    && cp ./api/settings.py.example ./api/settings.py \
    && sed -i "s#{user}:{password}@127.0.0.1:3306/{db}#cmdb:123456@mysql:3306/cmdb#g" api/settings.py \
    && sed -i "s#redis://127.0.0.1#redis://redis#g" api/settings.py \
    && sed -i 's#CACHE_REDIS_HOST = "127.0.0.1"#CACHE_REDIS_HOST = "redis"#g' api/settings.py

CMD ["bash", "-c", "flask run"]


# ================================= Search ================================
FROM docker.elastic.co/elasticsearch/elasticsearch:7.4.2 AS cmdb-search

RUN yes | ./bin/elasticsearch-plugin install https://github.com/medcl/elasticsearch-analysis-ik/releases/download/v7.4.2/elasticsearch-analysis-ik-7.4.2.zip
