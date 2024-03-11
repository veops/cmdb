### Install by Makefile

- Start mysql,redis
- Create mysql database: cmdb
- Pull code

  ```bash
  git clone https://github.com/veops/cmdb.git
  cd cmdb
  cp cmdb-api/settings.example.py cmdb-api/settings.py
  ```

  **set database in config file cmdb-api/settings.py**

- In cmdb directory,start in order as follows:
  - environment: `make env`
  - start API: `make api`
  - start UI: `make ui`
  - start worker: `make worker`
