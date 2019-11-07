FROM alpine:3.9

LABEL description="cmdb-ui"

RUN mkdir -p /data/apps/cmdb-ui/logs

COPY . /data/apps/cmdb-ui 

WORKDIR /data/apps/cmdb-ui

RUN apk add yarn && yarn install 

CMD ["sh", "-c", "yarn run serve"]
