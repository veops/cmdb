# Hướng Dẫn Cài Đặt CMDB Local Development

## 📋 Mục Lục

- [Yêu Cầu Hệ Thống](#yêu-cầu-hệ-thống)
- [Cài Đặt Từ Đầu Đến Cuối](#cài-đặt-từ-đầu-đến-cuối)
- [Khởi Chạy Hệ Thống](#khởi-chạy-hệ-thống)
- [Truy Cập Hệ Thống](#truy-cập-hệ-thống)
- [Troubleshooting](#troubleshooting)

## 🔧 Yêu Cầu Hệ Thống

### Hệ Điều Hành
- Ubuntu 20.04+ / Debian 11+ / CentOS 8+
- macOS 10.15+
- Windows 10+ (WSL2)

### Yêu Cầu Phần Mềm
- **Docker & Docker Compose** (cho MySQL và Redis)
- **Python 3.8 - 3.11**
- **Node.js 16+**
- **Git**

### Yêu Cầu Tài Nguyên
- RAM: Tối thiểu 4GB
- Disk: Tối thiểu 10GB
- CPU: 2 cores trở lên

## 🚀 Cài Đặt Từ Đầu Đến Cuối

### Bước 1: Cài Đặt Docker

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y docker.io docker-compose

# Khởi động Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Thêm user vào docker group (không cần sudo)
sudo usermod -aG docker $USER
# Logout và login lại để áp dụng
newgrp docker
```

### Bước 2: Cài Đặt Python

```bash
# Cài đặt Python 3.10
sudo apt install -y python3.10 python3.10-venv python3-pip

# Cài đặt pipenv
pip3 install pipenv

# Kiểm tra phiên bản
python3 --version
pipenv --version
```

### Bước 3: Cài Đặt Node.js

```bash
# Cài đặt Node.js 16
curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
sudo apt-get install -y nodejs

# Cài đặt Yarn
npm install -g yarn

# Kiểm tra phiên bản
node --version
npm --version
yarn --version
```

### Bước 4: Clone Repository

```bash
# Clone project
git clone https://github.com/veops/cmdb.git
cd cmdb

# Kiểm tra cấu trúc thư mục
ls -la
```

### Bước 5: Khởi Chạy Database Services (Docker)

```bash
# Tạo thư mục lưu trữ dữ liệu MySQL
mkdir -p ~/cmdb_data/mysql

# Khởi chạy MySQL
docker run -d \
  --name mysql-cmdb \
  -p 3306:3306 \
  -e MYSQL_ROOT_PASSWORD=Root_321 \
  -v ~/cmdb_data/mysql:/var/lib/mysql \
  mysql:8.0

# Khởi chạy Redis
docker run -d \
  --name redis-cmdb \
  -p 6379:6379 \
  redis:7-alpine

# Kiểm tra containers đang chạy
docker ps
```

### Bước 6: Cấu Hình MySQL

```bash
# Đợi MySQL khởi động hoàn tất (khoảng 30 giây)
sleep 30

# Cấu hình SQL mode
docker exec mysql-cmdb mysql -uroot -pRoot_321 -e "
SET GLOBAL sql_mode='STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
SET SESSION sql_mode='STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
"

# Tạo database
docker exec mysql-cmdb mysql -uroot -pRoot_321 -e "CREATE DATABASE cmdb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# Tạo user và cấp quyền
docker exec mysql-cmdb mysql -uroot -pRoot_321 -e "
CREATE USER 'cmdb'@'%' IDENTIFIED BY '123456';
GRANT ALL PRIVILEGES ON cmdb.* TO 'cmdb'@'%';
FLUSH PRIVILEGES;
"
```

### Bước 7: Cấu Hình Backend

```bash
# Vào thư mục backend
cd cmdb-api

# Copy file cấu hình
cp settings.example.py settings.py

# Tạo file .env cho development
cat > .env << EOF
FLASK_ENV=development
SECRET_KEY=dev-secret-key-change-in-production
MYSQL_USER=cmdb
MYSQL_PASSWORD=123456
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_DATABASE=cmdb
CACHE_REDIS_HOST=127.0.0.1
CACHE_REDIS_PORT=6379
CACHE_REDIS_PASSWORD=
EOF

# Cài đặt Python dependencies
pipenv install --dev

# Khởi tạo database
pipenv run flask db-setup
pipenv run flask common-check-new-columns
pipenv run flask cmdb-init-cache

# Import dữ liệu mẫu (tùy chọn)
docker exec -i mysql-cmdb mysql -ucmdb -p123456 cmdb < ../docs/cmdb.sql
```

### Bước 8: Cấu Hình Frontend

```bash
# Vào thư mục frontend
cd ../cmdb-ui

# Cài đặt Node.js dependencies
yarn install

# Tạo file cấu hình môi trường
cat > .env.development << EOF
NODE_ENV=development
VUE_APP_ENV=development
VUE_APP_API_BASE_URL=http://localhost:5000
VUE_APP_HOT_RELOAD=true
VUE_APP_DEV_SERVER_PORT=8000
VUE_APP_DEBUG=true
VUE_APP_USE_ENCRYPTION=false
EOF
```

## 🚀 Khởi Chạy Hệ Thống

### Terminal 1: Backend API Server

```bash
cd cmdb-api
pipenv run flask run -h 0.0.0.0 -p 5000
```

### Terminal 2: Frontend Development Server

```bash
cd cmdb-ui
yarn dev
```

### Terminal 3: Celery Workers (Async Tasks)

```bash
cd cmdb-api

# Worker cho CMDB tasks
pipenv run celery -A celery_worker.celery worker \
  -E -Q one_cmdb_async \
  --autoscale=5,2 \
  --logfile=one_cmdb_async.log -D

# Worker cho ACL tasks
pipenv run celery -A celery_worker.celery worker \
  -E -Q acl_async \
  --autoscale=2,1 \
  --logfile=one_acl_async.log -D
```

## 🌐 Truy Cập Hệ Thống

### URLs
- **Frontend:** http://localhost:8000
- **Backend API:** http://localhost:5000
- **API Documentation:** http://localhost:5000/api/docs

### Tài Khoản Mặc Định
- **Username:** `demo` hoặc `admin`
- **Password:** `123456`

## 🛠️ Lệnh Hữu Ích

### Kiểm Tra Trạng Thái Services

```bash
# Kiểm tra Docker containers
docker ps

# Kiểm tra logs MySQL
docker logs mysql-cmdb

# Kiểm tra logs Redis
docker logs redis-cmdb

# Kiểm tra kết nối MySQL
docker exec mysql-cmdb mysql -ucmdb -p123456 -e "SELECT 1;"

# Kiểm tra kết nối Redis
docker exec redis-cmdb redis-cli ping
```

### Quản Lý Database

```bash
# Backup database
docker exec mysql-cmdb mysqldump -ucmdb -p123456 cmdb > backup.sql

# Restore database
docker exec -i mysql-cmdb mysql -ucmdb -p123456 cmdb < backup.sql

# Reset database
docker exec mysql-cmdb mysql -ucmdb -p123456 -e "DROP DATABASE cmdb; CREATE DATABASE cmdb;"
```

### Development Commands

```bash
# Restart backend
cd cmdb-api
pipenv run flask run -h 0.0.0.0 -p 5000

# Restart frontend
cd cmdb-ui
yarn dev

# Restart workers
cd cmdb-api
pkill -f celery
pipenv run celery -A celery_worker.celery worker -E -Q one_cmdb_async --autoscale=5,2 --logfile=one_cmdb_async.log -D
pipenv run celery -A celery_worker.celery worker -E -Q acl_async --autoscale=2,1 --logfile=one_acl_async.log -D
```

## 🔍 Troubleshooting

### Lỗi Thường Gặp

#### 1. Port đã được sử dụng
```bash
# Kiểm tra port đang sử dụng
sudo netstat -tulpn | grep :8000
sudo netstat -tulpn | grep :5000

# Kill process
sudo kill -9 <PID>
```

#### 2. Database connection failed
```bash
# Kiểm tra MySQL container
docker ps | grep mysql

# Restart MySQL container
docker restart mysql-cmdb

# Kiểm tra logs
docker logs mysql-cmdb
```

#### 3. Redis connection failed
```bash
# Kiểm tra Redis container
docker ps | grep redis

# Restart Redis container
docker restart redis-cmdb

# Test kết nối
docker exec redis-cmdb redis-cli ping
```

#### 4. Python dependencies issues
```bash
# Xóa và cài lại virtual environment
cd cmdb-api
rm -rf ~/.virtualenvs/cmdb-api-*
pipenv install --dev
```

#### 5. Node.js dependencies issues
```bash
# Xóa node_modules và cài lại
cd cmdb-ui
rm -rf node_modules package-lock.json yarn.lock
yarn install
```

#### 6. Permission issues
```bash
# Cấp quyền cho thư mục logs
sudo mkdir -p cmdb-api/logs
sudo chown -R $USER:$USER cmdb-api/logs
```

### Log Files

```bash
# Backend logs
tail -f cmdb-api/logs/app.log

# Worker logs
tail -f cmdb-api/one_cmdb_async.log
tail -f cmdb-api/one_acl_async.log

# Docker logs
docker logs -f mysql-cmdb
docker logs -f redis-cmdb
```

### Performance Tuning

#### Database Optimization
```sql
-- Kết nối vào MySQL
docker exec -it mysql-cmdb mysql -ucmdb -p123456

-- Tăng performance
SET GLOBAL innodb_buffer_pool_size = 1073741824; -- 1GB
SET GLOBAL max_connections = 200;
SET GLOBAL query_cache_size = 67108864; -- 64MB
```

#### Redis Optimization
```bash
# Cấu hình Redis memory
docker exec redis-cmdb redis-cli CONFIG SET maxmemory 256mb
docker exec redis-cmdb redis-cli CONFIG SET maxmemory-policy allkeys-lru
```

## 🧹 Dọn Dẹp

### Dừng Hệ Thống
```bash
# Dừng backend và frontend (Ctrl+C trong terminals)

# Dừng workers
pkill -f celery

# Dừng Docker containers
docker stop mysql-cmdb redis-cmdb
```

### Xóa Hoàn Toàn
```bash
# Xóa containers và volumes
docker stop mysql-cmdb redis-cmdb
docker rm mysql-cmdb redis-cmdb
docker volume prune

# Xóa dữ liệu
rm -rf ~/cmdb_data

# Xóa virtual environments
rm -rf ~/.virtualenvs/cmdb-api-*
```

## 📚 Tài Liệu Tham Khảo

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Vue.js Documentation](https://vuejs.org/guide/)
- [Ant Design Vue](https://antdv.com/docs/vue/introduce)
- [Docker Documentation](https://docs.docker.com/)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [Redis Documentation](https://redis.io/documentation)

## 🤝 Hỗ Trợ

- **Email:** bd@veops.cn
- **GitHub Issues:** [https://github.com/veops/cmdb/issues](https://github.com/veops/cmdb/issues)
- **Documentation:** [https://veops.cn/docs/](https://veops.cn/docs/)

## 📝 Ghi Chú

- Đảm bảo Docker service đang chạy trước khi khởi chạy database containers
- Nếu gặp lỗi permission, hãy logout và login lại sau khi thêm user vào docker group
- Luôn backup database trước khi thực hiện các thay đổi lớn
- Kiểm tra logs thường xuyên để phát hiện và xử lý lỗi sớm 


cd cmdb-api && export PATH="$HOME/.local/bin:$PATH" && pipenv run flask run -h 0.0.0.0 -p 5000