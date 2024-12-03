
<h2 align="center">Simple, lightweight, and versatile operational CMDB</h2>
<p align="center">
  <a href="https://github.com/veops/cmdb/blob/master/LICENSE"><img src="https://img.shields.io/badge/License-AGPLv3-brightgreen" alt="License: GPLv3"></a>
  <a href="https:https://github.com/sendya/ant-design-pro-vue"><img src="https://img.shields.io/badge/UI-Ant%20Design%20Pro%20Vue-brightgreen" alt="UI"></a>
  <a href="https://github.com/pallets/flask"><img src="https://img.shields.io/badge/API-Flask-brightgreen" alt="API"></a>
</p>


------------------------------

[English](README_en.md) / [中文](../README.md)

## DEMO ONLINE
- Product document：https://veops.cn/docs/
- Preview online: <a href="https://cmdb.veops.cn" target="_blank">CMDB</a>
  - username: demo
  - password: 123456

> **ATTENTION**: branch `master` may be unstable as the result of continued development, please pull code from [releases](https://github.com/veops/cmdb/releases)

## Overview


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

- Custom models and model relationships, with model attributes supporting advanced features such as dropdown lists, font colors, and computed attributes.
- Support for automatic discovery of computers, network devices, storage devices, databases, middleware, public cloud resources, etc.
- Support for displaying resource, hierarchy, and relationship views.
- Fine-grained access control and comprehensive operation logs.
- General resource and relationship search capabilities.
- Support for IP Address Management (IPAM) and Data Center Infrastructure Management (DCIM).



### More Features

> Welcome to visit VeOps official website to discover more free operations and maintenance systems.

## Installation

### One-Click Docker Quick Build

[//]: # (> Method 1)
- step 1: **Prepare: install Docker and Docker Compose (v2)**
- step 2:  copy the repository
```shell 
git clone https://github.com/veops/cmdb.git
```
- step 3: In directory cmdb:
```
docker compose up -d
```

[//]: # (> M**ethod 2  Usefull for linux os.)

[//]: # (- step 1: **Prepare: install Docker and Docker Compose &#40;v2&#41;**)

[//]: # (- step 2: directly use the install.sh file in the project's root directory to `install`, `start`, `pause`, `status`, `delete`, and `uninstall` the application. )

[//]: # (```shell)

[//]: # (curl -so install.sh https://raw.githubusercontent.com/veops/cmdb/master/install.sh )

[//]: # (sh install.sh install)

[//]: # (```**)


### [Local Setup](local_en.md)

### [Installation with Makefile](makefile_en.md)

## Validation

- View: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- username: demo or admin
- password: 123456

## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-feature`)
5. Create new Pull Request

---
