**CMDB接口文档v0.1**   @ [维易科技](https://veops.cn)

# <div style="text-align: center;">CMDB接口文档</div>

### 一、CI接口

#### 1. CI查询接口

**条件搜索CI**, 按照模型的属性进行条件过滤、统计、排序等查询

* GET `/api/v0.1/ci/s`
* 参数
  
  | 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
  | ----  | ----   | ------   | ------ | ----|
  | **q** | q=private_ip:192* | string | 是 | 搜索表达式 |
  | **fl** |  | string | 否 | 返回的属性字段, 逗号分隔 |
  | **facet** | facet=idc | string | 否 | 属性字段，逗号分隔，返回属性对应的所有值的统计 |
  | **count** | count=1 | int | 否 | 一页返回的CI数, 默认是25 |
  | **page** | page=1 | int | 否 | 页数, 默认是1 |
  | **sort** |  sort=-private_ip| string | 否 | 属性的排序，降序字段前面加负号- |
  | **ret_key** | ret_key=name | enum | 否 | 返回字段类型, 可以是`id`、`name`、`alias`, 默认`name` |
  
* 参数**q**说明：
    * `_type` 指定CI模型, 多个用分号分隔. 例如: `_type:(server;vserver)`
    * `attribute:value` 指定属性搜索， `attribute`可以是`id`,`attr_name`和`attr_alias`
    * 以上的组合，逗号分隔
    * 组合查询使用方法
        * **`与`** 关系: `默认关系`
        * **`或`**关系: 属性字段前加`-`, 例如: `-hostname:cmdb*`、
        * **`非`**关系: 属性字段前加`~` 例如: `~hostname:cmdb*`
        * **`或非`**关系: 属性字段前加`-~` 例如: `-~hostname:*`
        * **`IN`**查询: 例如: `hostname:(cmdb*;cmdb-web*)` 小括号, 分号分隔
        * **`范围`**查询: 例如: `hostname:[cmdb* _TO_ cmdb-web*]` `_TO_`分隔
        * **`比较`**查询: 例如: `cpu_count:>5` 支持`>, >=, <, <=`
    * 多个条件可以用`小括号`进行组合

* 结果字段说明

  | 字段名 | 值的类型 | 说明 |
  | ----  | ----  | ----|
  | **numfound** |  int | CI总数 |
  | **total** |  int | 当前页的CI数 |
  | **page** |  int |分页 |
  | **result** | list | 返回的CI列表 |
  | **facet** | dict| 根据参数facet做的聚合统计|
  | **counter** |  dict | 当前页按模型的分类统计 |
  
* 返回结果
    * 搜索示例 `/api/v0.1/ci/s?q=_type:server,private_ip:192.*,idc:*,status:在线&sort=-private_ip&facet=idc&page=1&count=1`
    * 返回数据（默认json）
---
```json
{
  "counter": {
    "server": 1
  },
  "facet": {
    "idc": [
      [
        "南汇",
        600,
        "idc"
      ],
      [
        "外高桥",
        600,
        "idc"
      ],
      [
        "张江",
        600,
        "idc"
      ]
    ]
  },
  "numfound": 1800,
  "page": 1,
  "result": [
    {
      "_id": 7238,
      "_type": 4,
      "buy_date": null,
      "ci_type": "server",
      "cpu": "Intel(R) Xeon(R) CPU E5-2630 v4 @ 2.20GHz",
      "cpu_count": 20,
      "device_spec": "PowerEdge R630",
      "env": "test",
      "idc": "外高桥",
      "ilo_ip": "192.168.0.120",
      "ilo_mac": "82:7b:eb:f8:cb:03",
      "kernel_version": "4.1.12-61.1.33.el6uek.x86_64",
      "logic_cpu_count": 40,
      "maintain_enddate": null,
      "maintain_startdate": null,
      "manufacturer": "DELL",
      "op_duty": "张三",
      "os_version": "CentOS Linux release 7.6.1810 (Core)",
      "perm": null,
      "pos": null,
      "private_ip": "192.168.66.99",
      "rack": "12086",
      "raid": "1.089TB/RAID5",
      "ram": "128GB",
      "ram_size": "128GB",
      "rd_duty": "李四",
      "server_name": "192.168.66.99",
      "sn": "8cbe16404c11",
      "status": "在线",
      "unique": "sn",
      "vnc_port": null
    }
  ],
  "total": 1
}
```

#### 2. 新增CI接口

**创建或者修改CI**

* POST `/api/v0.1/ci` 
* 参数

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| ----  | ----   | ------   | ------ | ----|
| **ci_type** | ci_type=server | string | 是 | 创建CI所属的模型名 |
| **no_attribute_policy** | no_attribute_policy=ignore | string | 否 | 当添加不存在的attribute时的策略, 可选: `reject`、`ignore`, 默认`ignore` |
| **exist_policy** | exist_policy=reject | string | 否 | CI已经存在的处理策略, 可选: `need`、`reject`、`replace` 默认`reject` |
| **模型的属性名** | sn=xxxx | string | 否 | 属性名(id或别名亦可) |

> 注意: 请求的参数里必须包含该CI的唯一标识

* 返回结果

  ```json
  {
      "ci_id": 1
  }
  ```

#### 3. 修改CI接口

**修改CI**, 可以使用新增CI的接口, exist_policy=replace, 或者根据ci_id来修改

* PUT `/api/v0.1/ci` 或者 `/api/v0.1/ci/<int:ci_id>`
* 参数

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| ----  | ----   | ------   | ------ | ----|
| **ci_type** | ci_type=server | string | 是 | 创建CI所属的模型名 |
| **no_attribute_policy** | no_attribute_policy=ignore | string | 否 | 当添加不存在的attribute时的策略, 可选: `reject`、`ignore`, 默认`ignore` |
| **模型的属性名** | sn=xxxx | string | 否 | 属性名(id或别名亦可) |

> 注意: 如果使用`/api/v0.1/ci`, 请求的参数里必须包含该CI的唯一标识

* 返回结果

  ```json
  {
      "ci_id": 1
  }
  ```

#### 4. 删除CI接口

**根据ci_id删除CI**, 硬删除操作

* DELETE `/api/v0.1/ci/<int:ci_id>`
* 参数 无
* 返回结果

  ```json
  {
      "message": "ok"
  }
  ```

<div STYLE="page-break-after: always;"></div>

### 二、CI关系接口

#### 1. CI关系查询接口

**搜索所有的CI之间的关系**, 比如某一个事业部的所有应用或者是所有服务器

* GET `/api/v0.1/ci_relations/s`
* 参数
  
    | 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
    | ----  | ----   | ------   | ------ | ----|
    | **root_id** | root_id=1 | int | 是 | 根节点的ci_id |
    | **level** | level=1 | string | 否 | 关系的层级，多层用逗号分隔 |
    | **reverse** | reverse=0 | int | 否 | 是否反向搜索, 0或者1, 默认是0,  |
    | **q** | q=hostname:cmdb* | string | 否 | 搜索表达式 |
    | **fl** |  | string | 否 | 返回的属性字段, 逗号分隔 |
    | **facet** |  | string | 否 | 属性字段，逗号分隔，返回属性对应的所有值的统计 |
    | **count** | count=25 | int | 否 | 一页返回的CI数, 默认是25 |
    | **page** | page=1 | int | 否 | 页数, 默认是1 |
    | **sort** |  | string | 否 | 属性的排序，降序字段前面加负号- |
    | **ret_key** | | enum | 否 | 返回字段类型, 可以是`id`、`name`、`alias`, 默认`name` |
    
> 搜索表达式`q` 和 `CI查询接口`的搜索表达式q 完全一样!

* 结果字段说明

  | 字段名 | 值的类型 | 说明 |
  | ----  | ----  | ----|
  | **numfound** |  int | CI总数 |
  | **total** |  int | 当前页的CI数 |
  | **page** |  int |分页 |
  | **result** | list | 返回的CI列表 |
  | **facet** | dict| 根据参数facet做的聚合统计|
  | **counter** |  dict | 当前页按模型的分类统计 |
  
* 返回结果
    * 搜索某个事业部下面的物理机 `/api/v0.1/ci_relations/s?root_id=5&level=3&count=1&q=_type:server,idc:南汇`
    * 返回数据（默认json)    
---

```json
{
  "counter": {
    "server": 1
  },
  "facet": {},
  "numfound": 400,
  "page": 1,
  "result": [
    {
      "_id": 159,
      "_type": 4,
      "bu": null,
      "buy_date": null,
      "ci_type": "server",
      "cmc_ip": null,
      "cnc_ip": null,
      "cpu": "Intel(R) Xeon(R) CPU E5-2630 v4 @ 2.20GHz",
      "cpu_count": 20,
      "ctc_ip": null,
      "device_spec": "PowerEdge R630",
      "env": "prod",
      "idc": "南汇",
      "ilo_ip": "192.168.0.120",
      "ilo_mac": "82:7b:eb:f8:cb:03",
      "kernel_version": "4.1.12-61.1.33.el6uek.x86_64",
      "logic_cpu_count": 40,
      "maintain_enddate": null,
      "maintain_startdate": null,
      "manufacturer": "DELL",
      "oneagent_id": null,
      "op_duty": "张三",
      "os_version": "Microsoft Windows Server 2019 Standard",
      "perm": null,
      "pos": null,
      "private_ip": "192.168.1.2",
      "rack": "12086",
      "raid": "1.089TB/RAID5",
      "ram": "128GB",
      "ram_size": "128GB",
      "rd_duty": "李四",
      "server_name": "192.168.1.2",
      "server_room": null,
      "sn": "1fd3b1d5c253",
      "ssh_port": null,
      "status": "在线",
      "unique": "sn",
      "vnc_port": null
    }
  ],
  "total": 1
}
```

#### 2. 增加CI关系接口

**新增CI关系**, 参数`src_ci_id`是源CI的id, `dst_ci_id`是目标CI的id

* POST `/api/v0.1/ci_relations/<int:src_ci_id>/<int:dst_ci_id>`
* 参数 无
* 返回结果

  ```json
  {
      "cr_id": 1
  }
  ```

#### 3. 删除CI关系接口

**根据`cr_id`删除CI关系**, 参数`cr_id`是CI关系的id

* DELETE `/api/v0.1/ci_relations/<int:cr_id>` 
* 参数 无
* 返回结果

  ```json
  {
      "message": "CIType relation deleted"
  }
  ```

<div STYLE="page-break-after: always;"></div>

### 三、响应状态码说明

|状态码|说明|
|----|---|
|200|成功|
|400|请求参数错误或者失败|
|401|未认证|
|403|权限不够|
|404|访问的资源不存在|
|500|服务端未知错误|
|502|服务未启动或者异常退出|

> 所有错误或者失败，统一返回json格式为:
  ```json
  {
      "message": "错误描述"
  }
  ```


<div STYLE="page-break-after: always;"></div>

### 四、API鉴权方法
- 每个用户会自动生成一个 `api key` 和 一个`secret`, 在ACL系统里可查看到
- 调用API的时候，需要提供2个参数 `_key`和`_secret`
  - `_key`的值为您的`api key`
  - `_secret`的计算方法：
    - 除`_key`以外的参数，把**参数名**排序后参数值拼接在一起，并连接到`url path` + `secret`之后 
    - 求`sha1`**十六进制**值, 即sha1(`url path` + `secret` + `参数名排序后拼接的参数值`)的16进制值


### 五、Python调用样例
#### 鉴权
```python
import hashlib

key = "Your API key"
secret = "Your API secret"

def build_api_key(path, params):
    values = "".join([str(params[k]) for k in sorted(params.keys())
                      if params[k] is not None and not k.startswith('_')]) if params.keys() else ""
    _secret = "".join([path, secret, values]).encode("utf-8")
    params["_secret"] = hashlib.sha1(_secret).hexdigest()
    params["_key"] = key
    
    return params
```

#### 查询
* 以查询CI为例
```python
import hashlib

import requests
from future.moves.urllib.parse import urlparse

URL = "https://demo.veops.cn/api/v0.1/ci/s"
KEY = "Your API key"
SECRET = "Your API secret"


def build_api_key(path, params):
    values = "".join([str(params[k]) for k in sorted(params.keys())
                      if params[k] is not None and not k.startswith('_')]) if params.keys() else ""
    _secret = "".join([path, SECRET, values]).encode("utf-8")
    params["_secret"] = hashlib.sha1(_secret).hexdigest()
    params["_key"] = KEY

    return params


def get_ci(payload):
    payload = build_api_key(urlparse(URL).path, payload)

    return requests.get(URL, params=payload).json()

```

#### 增、删、改
* 以CI的增、删、改为例
```python
import hashlib

import requests
from future.moves.urllib.parse import urlparse

URL = "https://demo.veops.cn/api/v0.1/ci"
KEY = "Your API key"
SECRET = "Your API secret"


def build_api_key(path, params):
    values = "".join([str(params[k]) for k in sorted(params.keys())
                      if params[k] is not None and not k.startswith('_')]) if params.keys() else ""
    _secret = "".join([path, SECRET, values]).encode("utf-8")
    params["_secret"] = hashlib.sha1(_secret).hexdigest()
    params["_key"] = KEY

    return params


def add_ci(payload):
    payload = build_api_key(urlparse(URL).path, payload)

    return requests.post(URL, json=payload).json()


def update_ci(payload, ci_id=None):
    url = "{url}/{ci_id}".format(url=URL, ci_id=ci_id) if ci_id is not None else URL

    payload = build_api_key(urlparse(url).path, payload)

    return requests.put(url, json=payload).json()


def delete_ci(ci_id):
    url = "{url}/{ci_id}".format(url=URL, ci_id=ci_id)

    payload = build_api_key(urlparse(url).path, {})

    return requests.delete(url, json=payload).json()

```
