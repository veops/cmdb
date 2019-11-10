FROM node:alpine as builder

LABEL description="cmdb-ui"

COPY . /data/apps/cmdb-ui 

WORKDIR /data/apps/cmdb-ui

RUN sed -i 's#http://127.0.0.1:5000##g' .env && yarn install  && yarn build


FROM nginx:latest

RUN apt-get update && apt-get install -y curl && apt-get clean

RUN mkdir /etc/nginx/html

COPY --from=builder /data/apps/cmdb-ui/dist /etc/nginx/html/
