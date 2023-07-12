## Install by Makefile

- 启动 mysql 服务, redis 服务

- 创建数据库 cmdb
- 拉取代码

```bash
git clone https://github.com/veops/cmdb.git
cd cmdb
cp cmdb-api/settings.example.py cmdb-api/settings.py
```

**设置 cmdb-api/settings.py 里的 database**

- 顺序在 cmdb 目录下执行
  - 环境: `make env`
  - 启动 API: `make api`
  - 启动 UI: `make ui`
  - 启动 worker: `make worker`
