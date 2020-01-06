# CMDB查询 API文档



## 用户接口

### CI通用搜索接口
##### 搜索所有的CI实例

* GET `/api/v0.1/ci/s`
* 参数
    * `string:_type` 搜索的ci_type，多个用分号隔开, 例如: _type:(docker;kvm)
    * `string:q` 搜索表达式, 例如`q=hostname:cmdb*`
    * `string:fl` 返回字段(id, attr_name, attr_alias均可)，英文半角逗号分隔
    * `string:ret_key` 返回字段类型 `Enum("id", "name", "alias")` 默认 `name`
    * `count` 指定一次返回CI数
    * `facet` 属性字段，逗号分隔，返回属性字段对应的所有值
    
* 搜索表达式：
    * 简单的字符串
    * `attribute:value` 指定属性搜索， `attribute`可以是`id`,`attr_name`和`attr_alias`
    * 以上的组合，逗号分隔
    
* 组合查询支持
    * `AND`关系-`默认关系`
    * `OR`关系 - eg.`-hostname:cmdb*`、
    * `NOT`关系-属性字段前加`~`eg. `~hostname:cmdb*`
    * `IN`查询. eg. `hostname:(cmdb*;cmdb-web*)` 小括号, 分号分隔
    * `RANGE`查询. eg. `hostname:[cmdb* _TO_ cmdb-web*]` `_TO_`分隔
    * `COMPARISON`查询. eg. `cpu_count:>5` 支持`>, >=, <, <=`
    
* 返回结果
    * 搜索表达式 `/api/v0.1/ci/s?q=_type:kvm,status:在线,idc:南汇,private_ip:10.1.1.1*&page=1&fl=hostname,private_ip&facet=private_ip&count=1`
    * 返回数据（默认json）
    
    ```
    {
        facet: {
            private_ip: [
                    [
                        "10.1.1.11",
                        1,
                        "private_ip"
                    ],
                    [
                        "10.1.1.12",
                        1,
                        "private_ip"
                    ],
                    [
                        "10.1.1.13",
                        1,
                        "private_ip"
                    ]
            ]
        },
        total: 1,
        numfound: 3,
        result: [
            {
                hostname: "xxx11",
                private_ip: [
                    "10.1.1.11"
                ]
            }
         ],
        counter: {
            kvm: 1
        },
        page: 1
    }
    ```  
         
### CI Relation通用搜索接口

##### 搜索所有的CI之间的关系，比如某一个产品线线的所有应用或者是所有服务器

* GET `/api/v0.1/ci_relations/s`
* 参数
    * `int:root_id` 搜索的根节点的ci_id
    * `int:level` 搜索的层级
    * `string:_type` 搜索的ci_type，多个用分号隔开, 例如: _type:(docker;kvm)
    * `string:q` 搜索表达式, 例如`q=hostname:cmdb*`
    * `string:fl` 返回字段(id, attr_name, attr_alias均可)，英文半角逗号分隔
    * `string:ret_key` 返回字段类型 `Enum("id", "name", "alias")` 默认 `name`
    * `count` 指定一次返回CI数
    * `facet` 属性字段，逗号分隔，返回属性字段对应的所有值
    
* 搜索表达式：
    * 简单的字符串
    * `attribute:value` 指定属性搜索， `attribute`可以是`id`,`attr_name`和`attr_alias`
    * 以上的组合，逗号分隔
    
* 组合查询支持
    * `AND`关系-`默认关系`
    * `OR`关系 - eg.`-hostname:cmdb*`、
    * `NOT`关系-属性字段前加`~`eg. `~hostname:cmdb*`
    * `IN`查询. eg. `hostname:(cmdb*;cmdb-web*)` 小括号, 分号分隔
    * `RANGE`查询. eg. `hostname:[cmdb* _TO_ cmdb-web*]` `_TO_`分隔
    * `COMPARISON`查询. eg. `cpu_count:>5` 支持`>, >=, <, <=`
    
* 返回结果
    * 搜索表达式 `/api/v0.1/ci_relations/s?root_id=53&level=3&q=_type:kvm,status:在线,idc:南汇,private_ip:10.1.1.1*&page=1&fl=hostname,private_ip&facet=private_ip&count=1`
    * 返回数据（默认json）
    
    ```
    {
        facet: {
            private_ip: [
                    [
                        "10.1.1.11",
                        1,
                        "private_ip"
                    ],
                    [
                        "10.1.1.12",
                        1,
                        "private_ip"
                    ],
                    [
                        "10.1.1.13",
                        1,
                        "private_ip"
                    ]
            ]
        },
        total: 1,
        numfound: 3,
        result: [
            {
                hostname: "xxx11",
                private_ip: [
                    "10.1.1.11"
                ]
            }
         ],
        counter: {
            kvm: 1
        },
        page: 1
    }  
    ```
        