FROM centos:7.6.1810

LABEL description="Python2.7.5,cmdb"

RUN mkdir -p /data/apps/cmdb ~/.pip /data/apps/cmdb/logs 

COPY .. /data/apps/cmdb 

WORKDIR /data/apps/cmdb

RUN mv /data/apps/cmdb/pip.conf ~/.pip/ \
	&&  yum install -y epel-release \
	&&  yum install -y python-pip \
    && pip install -r requirements.txt 

CMD ["bash", "-c", "cp api/settings.py.example api/settings.py && sed -i 's#{user}:{password}@127.0.0.1:3306/{db}#:@127.0.0.1:3306/cmdb#g' api/settings.py && flask run"]

