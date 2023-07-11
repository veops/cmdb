# ================================= UI ================================
FROM node:16.0.0-alpine AS builder

LABEL description="cmdb-ui"

COPY cmdb-ui /data/apps/cmdb-ui

WORKDIR /data/apps/cmdb-ui

RUN sed -i "s#http://127.0.0.1:5000##g" .env && yarn install  && yarn build


FROM nginx:alpine AS cmdb-ui

RUN mkdir /etc/nginx/html && rm -f /etc/nginx/conf.d/default.conf

COPY --from=builder /data/apps/cmdb-ui/dist /etc/nginx/html/


# ================================= API ================================
FROM python:3.8-alpine AS cmdb-api

LABEL description="Python3.8,cmdb"

COPY cmdb-api /data/apps/cmdb

WORKDIR /data/apps/cmdb

RUN apk add --no-cache tzdata gcc musl-dev libffi-dev openldap-dev python3-dev jpeg-dev zlib-dev build-base

ENV TZ=Asia/Shanghai

RUN pip install  --no-cache-dir -r requirements.txt \
    && cp ./settings.example.py settings.py \
    && sed -i "s#{user}:{password}@127.0.0.1:3306/{db}#cmdb:123456@mysql:3306/cmdb#g" settings.py \
    && sed -i "s#redis://127.0.0.1#redis://redis#g" settings.py \
    && sed -i 's#CACHE_REDIS_HOST = "127.0.0.1"#CACHE_REDIS_HOST = "redis"#g' settings.py

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.7.3/wait /wait
RUN chmod +x /wait

CMD ["bash", "-c", "flask run"]


# ================================= Search ================================
FROM docker.elastic.co/elasticsearch/elasticsearch:7.4.2 AS cmdb-search

RUN yes | ./bin/elasticsearch-plugin install https://github.com/medcl/elasticsearch-analysis-ik/releases/download/v7.4.2/elasticsearch-analysis-ik-7.4.2.zip
