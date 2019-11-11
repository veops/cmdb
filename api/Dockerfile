# build under cmdb directory other than api
# maybe use: cd ..
FROM centos:7.6.1810 AS cmdb-api

LABEL description="Python3.7.5,cmdb"

RUN mkdir -p /data/apps/cmdb /data/apps/cmdb/logs 

COPY . /data/apps/cmdb 

WORKDIR /data/apps/cmdb

RUN yum install -y epel-release && yum clean all\
	&&  yum install -y python-pip \
    && pip install  --no-cache-dir -r docs/requirements.txt \
    && cp ./api/settings.py.example ./api/settings.py \
    && sed -i "s#{user}:{password}@127.0.0.1:3306/{db}#cmdb:123456@mysql:3306/cmdb#g" api/settings.py \
    && sed -i "s/127.0.0.1/redis/g" api/settings.py

CMD ["bash", "-c", "flask run"]
