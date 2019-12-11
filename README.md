<h1 align="center">CMDB</h1>
<div align="center">
尽可能实现比较通用的运维资产数据的配置和管理
</div>

<div align="center">

[![License](https://img.shields.io/badge/License-GPLv2-brightgreen)](https://github.com/pycook/cmdb/blob/master/LICENSE)
[![UI](https://img.shields.io/badge/UI-Ant%20Design%20Pro%20Vue-brightgreen)](https://github.com/sendya/ant-design-pro-vue) 
[![API](https://img.shields.io/badge/API-Flask-brightgreen)](https://github.com/pallets/flask) 

</div>



- 在线预览: [CMDB](http://121.42.12.46:8000)
    - username: demo
    - password: 123456
    
> **重要提示**: `master` 分支在开发过程中可能处于 *不稳定的状态* 。
请通过[releases](https://github.com/pycook/cmdb/releases)获取
    
Overview
----
### 3种类型视图
1. 资源视图 - 模型的实例数据, 用户可订阅
2. 树形视图 - 模型按字段分级, 用树形图方式展示, 用户可订阅
3. 关系视图 - 模型之间的关系, 用树形图方式展示, **管理员可配置**

##### 资源视图
![基础资源视图](https://raw.githubusercontent.com/pycook/cmdb/master/ui/public/cmdb-ci.jpeg) 

##### 树形视图
![树形视图](https://raw.githubusercontent.com/pycook/cmdb/master/ui/public/cmdb-tree.jpeg) 

##### 关系视图
![关系视图](https://raw.githubusercontent.com/pycook/cmdb/master/ui/public/cmdb-relation.jpeg) 

##### 用户订阅
![用户订阅](https://raw.githubusercontent.com/pycook/cmdb/master/ui/public/cmdb-preference.jpeg)

##### 关系视图配置
![关系视图配置](https://raw.githubusercontent.com/pycook/cmdb/master/ui/public/cmdb-relation-define.jpeg)

Docker一键快速构建
----
- 进入主目录（先安装docker环境）
```
    docker-compose up -d
```

- 浏览器打开: [http://127.0.0.1:8000](http://127.0.0.1:8000)


本地搭建: 环境和依赖
----
- 存储: mysql, redis
- python版本: python2.7, >=python3.6

Install
----
- 启动mysql服务, redis服务

- 创建数据库cmdb
- 拉取代码
```bash
git clone https://github.com/pycook/cmdb.git
cd cmdb
cp api/settings.py.example api/settings.py
```
**设置api/settings.py里的database**

- 安装库
  - 后端: ```pipenv run pipenv install```
  - 前端: ```cd ui && yarn install && cd ..```
  
- 创建数据库表 ```pipenv run flask db-setup && pipenv run flask init-cache```
- 可以将docs/cmdb.sql导入到数据库里，登录用户和密码都是:admin
  
- 启动服务
  - 后端: ```pipenv run flask run -h 0.0.0.0```
  - 前端: ```cd ui && yarn run serve```
  - worker: ```celery worker -A celery_worker.celery -E -Q cmdb_async --concurrency=1```
  
  - 浏览器打开:  [http://127.0.0.1:8000](http://127.0.0.1:8000)
    - 如果是非本机访问, 要修改**ui/.env**里**VUE_APP_API_BASE_URL**里的IP地址为后端服务的ip地址


Install by Makefile
----
- 启动mysql服务, redis服务

- 创建数据库cmdb
- 拉取代码
```bash
git clone https://github.com/pycook/cmdb.git
cd cmdb
cp api/settings.py.example api/settings.py
```
**设置api/settings.py里的database**

- 顺序在cmdb目录下执行
    - 环境: ```make env```
    - 启动API: ```make api```
    - 启动UI: ```make ui```
    - 启动worker: ```make worker```


----
_**欢迎加入CMDB运维开发QQ群（336164978）**_

![QQ群](ui/public/qr_code.jpg)