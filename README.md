![基础资源视图](docs/logo.png)

[![License](https://img.shields.io/badge/License-AGPLv3-brightgreen)](https://github.com/veops/cmdb/blob/master/LICENSE)
[![UI](https://img.shields.io/badge/UI-Ant%20Design%20Pro%20Vue-brightgreen)](https://github.com/sendya/ant-design-pro-vue) 
[![API](https://img.shields.io/badge/API-Flask-brightgreen)](https://github.com/pallets/flask) 


[English](README_en.md) / [中文](README.md)

- 在线体验: <a href="https://cmdb.veops.cn" target="_blank">CMDB</a>
    - username: demo
    - password: 123456
    
> **重要提示**: `master` 分支在开发过程中可能处于 *不稳定的状态* 。
请通过[releases](https://github.com/veops/cmdb/releases)获取
    
系统介绍
-------------
### 整体架构
<img src=docs/view.png />

### 相关文档
- <a href="https://zhuanlan.zhihu.com/p/98453732" target="_blank">设计文档</a>
- <a href="https://github.com/veops/cmdb/tree/master/docs" target="_blank">API文档</a>
- <a href="https://mp.weixin.qq.com/s/EflmmJ-qdUkddTx2hRt3pA" target="_blank">树形视图实践</a>

### 特点
- 灵活性
   1. 规范并统一纳管复杂数据资产
   2. 自动发现、入库IT资产
- 安全性
  1. 细粒度访问控制
  2. 完备操作日志
- 多应用
  1. 丰富视图展示维度
  2. 提供Restful API
  3. 自定义字段触发器
  
### 主要功能
- 模型属性支持索引、多值、默认排序、字体颜色，支持计算属性
- 支持自动发现、定时巡检、文件导入
- 支持资源、树形、关系视图展示
- 支持模型间关系配置和展示
- 细粒度访问控制，完备的操作日志
- 支持跨模型搜索

### 系统概览
- 服务树
![1](docs/0.png "首页展示")

[查看更多展示](docs/screenshot.md)

### 更多功能

> 也欢迎移步[维易科技官网](https://www.veops.cn)，发现更多免费运维系统。

## 推荐项目
[Spug - 开源轻量自动化运维平台](https://github.com/openspug/spug)

安装
----
### [Docker一键快速构建](docs/docker.md)
### [本地搭建](docs/local.md)
### [Makefile安装](docs/makefile.md)


----------------------
_**欢迎加入CMDB运维开发QQ群（336164978）**_

![QQ群](docs/qr_code.jpg)
