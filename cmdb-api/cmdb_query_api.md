# CMDB查询 API文档



## 用户接口

### CI通用搜索接口

* GET `/api/v0.1/ci/s`
* 参数
    * `string:_type` 搜索的ci_type，多个用分号隔开, 例如: _type:(docker;kvm)
    * `string:q` 搜索表达式, 例如`q=hostname:cmdb*`
    * `string:fl` 返回字段(id, attr_name, attr_alias均可)，英文半角逗号分隔
    * `string:ret_key` 返回字段类型 `Enum("id", "name", "alias")` 默认 `name`
    * `count` 指定一次返回CI数
    * `facet` 属性字段，逗号分隔，返回属性字段对应的所有值
    * `wt` 返回的数据格式，默认为`json`, 可选参数为`xml`
    
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
                ci_type: "kvm",
                _type: 8,
                _id: 3213,
                hostname: "xxx11",
                private_ip: [
                    "10.1.1.11"
                ]
            },
            {
                ci_type: "kvm",
                _type: 8,
                _id: 123232,
                hostname: "xxx12",
                private_ip: [
                    "10.1.1.12"
                ]
            },
            {
                ci_type: "kvm",
                _type: 8,
                _id: 123513,
                hostname: "xxx13",
                private_ip: [
                    "10.1.1.13"
                ]
            }
         ],
        counter: {
            kvm: 3
        },
        page: 1
    }
```

                
### CI专用搜索接口   
##### 根据需求实现
    
        