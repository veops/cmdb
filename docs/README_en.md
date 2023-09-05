![维易CMDB](images/logo.png)

[![License](https://img.shields.io/badge/License-AGPLv3-brightgreen)](https://github.com/veops/cmdb/blob/master/LICENSE)
[![UI](https://img.shields.io/badge/UI-Ant%20Design%20Pro%20Vue-brightgreen)](https://github.com/sendya/ant-design-pro-vue)
[![API](https://img.shields.io/badge/API-Flask-brightgreen)](https://github.com/pallets/flask)

[English](README_en.md) / [中文](../README.md)

## DEMO ONLINE

- Preview online: <a href="https://cmdb.veops.cn" target="_blank">CMDB</a>
  - username: demo
  - password: 123456

> **ATTENTION**: branch `master` may be unstable as the result of continued development, please pull code from [releases](https://github.com/veops/cmdb/releases)

## Overview

### Technical Architecture

<img src=images/view.jpg />

### Document

- <a href="https://zhuanlan.zhihu.com/p/98453732" target="_blank">Design Document</a>
- <a href="https://github.com/veops/cmdb/tree/master/docs/cmdb_api.md" target="_blank">API Documentation</a>
- <a href="https://mp.weixin.qq.com/s/EflmmJ-qdUkddTx2hRt3pA" target="_blank">Practice of Tree View</a>

### Features

- Flexibility
  1. Standardize and manage complex data assets
  2. Automatically discover and inventory IT assets
- Security
  1. Fine-grained access control
  2. Comprehensive operation logs
- Multi-application
  1. Rich view display dimensions
  2. Provide Restful API
  3. Custom field triggers

### Main Features

- Model attributes support indexing, multiple values, default sorting, font color, and computed properties.
- Support automatic discovery, scheduled inspections, and file import.
- Support resource, tree view, and relationship view display.
- Support configuration and display of relationships between models.
- Fine-grained access control and comprehensive operation logs.
- Support cross-model search.

### System Overview

- Service Tree
  ![1](images/0.png "首页展示")

[View more screenshots](screenshot.md)

### More Features

> Welcome to visit VeOps official website to discover more free operations and maintenance systems.

## Installation

### One-Click Docker Quick Build

- Prepare: install docker and docker-compose
- In directory cmdb
  ```
  docker-compose up -d
  ```
- View: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- username: demo or admin
- password: 123456


### [Local Setup](local_en.md)

### [Installation with Makefile](makefile_en.md)

## Contributing

1. Fork it
1. Create your feature branch (`git checkout -b my-feature`)
1. Commit your changes (`git commit -am 'Add some feature'`)
1. Push to the branch (`git push origin my-feature`)
1. Create new Pull Request

---

_**Welcome to pay attention to our public account, click to contact us, join WeChat, QQ operation and maintenance group, and get more product and industry related information**_

![QQgroup](images/qrcode_for_gzh.jpg)
