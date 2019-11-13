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

RUN apk add --no-cache gcc musl-dev libffi-dev

RUN pip install  --no-cache-dir -r docs/requirements.txt \
    && cp ./api/settings.py.example ./api/settings.py \
    && sed -i "s#{user}:{password}@127.0.0.1:3306/{db}#cmdb:123456@mysql:3306/cmdb#g" api/settings.py \
    && sed -i "s/127.0.0.1/redis/g" api/settings.py

CMD ["bash", "-c", "flask run"]