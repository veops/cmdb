## 使用Flask-Migrate做数据库版本管理

- 首次可以删除cmdb-api/migrations/versions下的所有文件
- 

### 进入cmdb-api完成下面步骤（操作可能会删除数据库中不被代码管理的表，如需保留请看文末中的tips）

- 如果是首次使用需要先删除cmdb-api/migrations/versions下的所有文件（非首次跳过）
- 执行`flask db migrate` 生成对应版本数据库表的升级文件到versions文件夹下，需要你的数据库是已经upgrade的
- 执行`flask db upgrade` 数据库表同步更新到mysql


### tips

- cmdb-api/migrations/env.py文件内的exclude_tables列表可以填写不想被flask-migrate管理的数据库表
