
<p align="center">
  <a href="https://veops.cn"><img src="docs/images/logo.png" alt="维易CMDB" width="300"/></a>
</p>
<h3 align="center">简单、轻量、通用的运维配置管理数据库</h3>
<p align="center">
  <a href="https://github.com/veops/cmdb/blob/master/LICENSE"><img src="https://img.shields.io/badge/License-AGPLv3-brightgreen" alt="License: GPLv3"></a>
  <a href="https:https://github.com/sendya/ant-design-pro-vue"><img src="https://img.shields.io/badge/UI-Ant%20Design%20Pro%20Vue-brightgreen" alt="UI"></a>
  <a href="https://github.com/pallets/flask"><img src="https://img.shields.io/badge/API-Flask-brightgreen" alt="API"></a>
</p>


------------------------------

[English](docs/README_en.md) / [中文](README.md)
- 产品文档：https://veops.cn/docs/
- 在线体验：<a href="https://cmdb.veops.cn" target="_blank">CMDB</a>
  - username: demo 或者 admin
  - password: 123456

> **重要提示**: `master` 分支在开发过程中可能处于 _不稳定的状态_ 。
> 请通过[releases](https://github.com/veops/cmdb/releases)获取

## 系统介绍

### 系统概览

<img src=docs/images/dashboard.png />

[查看更多展示](docs/screenshot.md)

### 相关文章

- <a href="https://mp.weixin.qq.com/s/v3eANth64UBW5xdyOkK3tg" target="_blank">概要设计</a>
- <a href="https://github.com/veops/cmdb/tree/master/docs/cmdb_api.md" target="_blank">API 文档</a>
- <a href="https://mp.weixin.qq.com/s/rQaf4AES7YJsyNQG_MKOLg" target="_blank">自动发现</a>
- 更多文章可以在公众号 **维易科技OneOps** 里查看

### 特点

- 灵活性
  1. 配置灵活，不设定任何运维场景，有内置模板
  2. 自动发现、入库 IT 资产
- 安全性
  1. 细粒度权限控制
  2. 完备操作日志
- 多应用
  1. 丰富视图展示维度
  2. API简单强大
  3. 支持定义属性触发器、计算属性

### 主要功能

- 模型属性支持索引、多值、默认排序、字体颜色，支持计算属性
- 支持自动发现、定时巡检、文件导入
- 支持资源、层级、关系视图展示
- 支持模型间关系配置和展示
- 细粒度访问控制，完备的操作日志
- 支持跨模型搜索





### 更多功能

> 也欢迎移步[维易科技官网](https://veops.cn)，发现更多免费运维系统。

## 接入公司

> 欢迎使用开源CMDB的公司，在 [#112](https://github.com/veops/cmdb/issues/112) 登记

## 安装

### Docker 一键快速构建
> 方法一
- 第一步: 先安装 Docker 环境, 以及Docker Compose (v2)
- 第二步: 拷贝项目
```shell 
git clone https://github.com/veops/cmdb.git
```
- 第三步：进入主目录，执行:
```
docker compose up -d
```
> 方法二, 该方法适用于linux系统
- 第一步： 先安装 Docker 环境, 以及Docker Compose (v2)
- 第二步： 直接使用项目根目录下的install.sh 文件进行 `安装`、`启动`、`暂停`、`查状态`、`删除`、`卸载`
```shell
curl -so install.sh https://raw.githubusercontent.com/veops/cmdb/master/install.sh
sh install.sh install
```

### [本地开发环境搭建](docs/local.md)

### [Makefile 安装](docs/makefile.md)

## 验证
- 浏览器打开: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- username: demo 或者 admin
- password: 123456


---

_**欢迎关注公众号(维易科技OneOps)，关注后可加入微信群，进行产品和技术交流。**_

![公众号: 维易科技OneOps](docs/images/wechat.png)
