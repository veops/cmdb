# CMDB API文档

```
Rule                                                               Endpoint
------------------------------------------------------------------------------------------------------------
/api/login                                                         account_api.loginview
/api/logout                                                        account_api.logoutview
/api/sso/login                                                     cas.login
/api/sso/logout                                                    cas.logout
/api/v0.1/attributes                                               cmdb_api_v01.attributeview
/api/v0.1/attributes/<int:attr_id>                                 cmdb_api_v01.attributeview
/api/v0.1/attributes/<string:attr_name>                            cmdb_api_v01.attributeview
/api/v0.1/attributes/s                                             cmdb_api_v01.attributesearchview
/api/v0.1/attributes/search                                        cmdb_api_v01.attributesearchview
/api/v0.1/ci                                                       cmdb_api_v01.ciview
/api/v0.1/ci/<int:ci_id>                                           cmdb_api_v01.ciview
/api/v0.1/ci/<int:ci_id>/detail                                    cmdb_api_v01.cidetailview
/api/v0.1/ci/<int:ci_id>/flush                                     cmdb_api_v01.ciflushview
/api/v0.1/ci/<int:ci_id>/unique                                    cmdb_api_v01.ciunique
/api/v0.1/ci/flush                                                 cmdb_api_v01.ciflushview
/api/v0.1/ci/heartbeat                                             cmdb_api_v01.ciheartbeatview
/api/v0.1/ci/heartbeat/<string:ci_type>/<string:unique>            cmdb_api_v01.ciheartbeatview
/api/v0.1/ci/s                                                     cmdb_api_v01.cisearchview
/api/v0.1/ci/search                                                cmdb_api_v01.cisearchview
/api/v0.1/ci/type/<int:type_id>                                    cmdb_api_v01.cisbytypeview
/api/v0.1/ci_relations/<int:cr_id>                                 cmdb_api_v01.deletecirelationview
/api/v0.1/ci_relations/<int:first_ci_id>/<int:second_ci_id>        cmdb_api_v01.cirelationview
/api/v0.1/ci_relations/<int:first_ci_id>/second_cis                cmdb_api_v01.getsecondcisview
/api/v0.1/ci_relations/<int:second_ci_id>/first_cis                cmdb_api_v01.getfirstcisview
/api/v0.1/ci_relations/s                                           cmdb_api_v01.cirelationsearchview
/api/v0.1/ci_relations/search                                      cmdb_api_v01.cirelationsearchview
/api/v0.1/ci_relations/statistics                                  cmdb_api_v01.cirelationstatisticsview
/api/v0.1/ci_type_relations                                        cmdb_api_v01.cityperelationview
/api/v0.1/ci_type_relations/<int:child_id>/parents                 cmdb_api_v01.getparentsview
/api/v0.1/ci_type_relations/<int:ctr_id>                           cmdb_api_v01.cityperelationdelete2view
/api/v0.1/ci_type_relations/<int:parent_id>/<int:child_id>         cmdb_api_v01.cityperelationview
/api/v0.1/ci_type_relations/<int:parent_id>/children               cmdb_api_v01.getchildrenview
/api/v0.1/ci_types                                                 cmdb_api_v01.citypeview
/api/v0.1/ci_types/<int:type_id>                                   cmdb_api_v01.citypeview
/api/v0.1/ci_types/<int:type_id>/attribute_groups                  cmdb_api_v01.citypeattributegroupview
/api/v0.1/ci_types/<int:type_id>/attributes                        cmdb_api_v01.citypeattributeview
/api/v0.1/ci_types/<int:type_id>/enable                            cmdb_api_v01.enablecitypeview
/api/v0.1/ci_types/<string:type_name>                              cmdb_api_v01.citypeview
/api/v0.1/ci_types/<string:type_name>/attributes                   cmdb_api_v01.citypeattributeview
/api/v0.1/ci_types/attribute_groups/<int:group_id>                 cmdb_api_v01.citypeattributegroupview
/api/v0.1/ci_types/groups                                          cmdb_api_v01.citypegroupview
/api/v0.1/ci_types/groups/<int:gid>                                cmdb_api_v01.citypegroupview
/api/v0.1/ci_types/query                                           cmdb_api_v01.citypequeryview
/api/v0.1/history/ci/<int:ci_id>                                   cmdb_api_v01.cihistoryview
/api/v0.1/history/records                                          cmdb_api_v01.recordview
/api/v0.1/history/records/<int:record_id>                          cmdb_api_v01.recorddetailview
/api/v0.1/preference/ci_types                                      cmdb_api_v01.preferenceshowcitypesview
/api/v0.1/preference/ci_types/<id_or_name>/attributes              cmdb_api_v01.preferenceshowattributesview
/api/v0.1/preference/relation/view                                 cmdb_api_v01.preferencerelationapiview
/api/v0.1/preference/tree/view                                     cmdb_api_v01.preferencetreeapiview
/api/v0.1/relation_types                                           cmdb_api_v01.relationtypeview
/api/v0.1/relation_types/<int:rel_id>                              cmdb_api_v01.relationtypeview
/api/v1/acl/resource_groups                                        acl_api_v1.resourcegroupview
/api/v1/acl/resource_groups/<int:group_id>                         acl_api_v1.resourcegroupview
/api/v1/acl/resource_groups/<int:group_id>/items                   acl_api_v1.resourcegroupitemsview
/api/v1/acl/resource_groups/<int:group_id>/permissions             acl_api_v1.resourcepermissionview
/api/v1/acl/resource_types                                         acl_api_v1.resourcetypeview
/api/v1/acl/resource_types/<int:type_id>                           acl_api_v1.resourcetypeview
/api/v1/acl/resource_types/<int:type_id>/perms                     acl_api_v1.resourcetypepermsview
/api/v1/acl/resources                                              acl_api_v1.resourceview
/api/v1/acl/resources/<int:resource_id>                            acl_api_v1.resourceview
/api/v1/acl/resources/<int:resource_id>/permissions                acl_api_v1.resourcepermissionview
/api/v1/acl/roles                                                  acl_api_v1.roleview
/api/v1/acl/roles/<int:child_id>/parents                           acl_api_v1.rolerelationview
/api/v1/acl/roles/<int:rid>                                        acl_api_v1.roleview
/api/v1/acl/roles/<int:rid>/resource_groups/<int:group_id>/grant   acl_api_v1.rolepermissiongrantview
/api/v1/acl/roles/<int:rid>/resource_groups/<int:group_id>/revoke  acl_api_v1.rolepermissionrevokeview
/api/v1/acl/roles/<int:rid>/resources/<int:resource_id>/grant      acl_api_v1.rolepermissiongrantview
/api/v1/acl/roles/<int:rid>/resources/<int:resource_id>/revoke     acl_api_v1.rolepermissionrevokeview
/api/v1/acl/users                                                  acl_api_v1.userview
/api/v1/acl/users/<int:uid>                                        acl_api_v1.userview
/api/v1/acl/users/info                                             acl_api_v1.getuserinfoview
/api/v1/acl/users/reset_key_secret                                 acl_api_v1.userresetkeysecretview
```

## 状态返回码的定义
* 200：成功
* 400：失败
* 401：未认证
* 403：no permission
* 404：not found
* 500：服务器未知错误


## 用户接口

### CI搜索接口

* GET `/api/v0.1/ci/s`
* 参数
    * `string:_type` 搜索的ci_type，多个用分号隔开, 例如: _type:(server;vservser)
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
    * `COMPARISON`查询. eg. `cpu_core_num:>5` 支持`>, >=, <, <=`

### CI Relation搜索接口
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
    
    
## api key 认证

每个用户会自动生成一个 `api key` 和 一个`secret`, 通过API接口使用的时候，需要提供一个参数 `_key`值为您的`api key`， 以及参数`_secret`值为除`_key`以外的参数，按照**参数名的字典序**排列，并连接到`url path` + `secret`之后的`sha1`**十六进制**值。


## 管理接口

### Attribute管理接口
* GET `/api/v0.1/attributes/s` 列出所有属性
    * param
        * `string:q` 属性名称或者别名，允许为空
    * return
    
    ```
    {
        "numfound": 1,
        "attributes": [
        {
            "attr_name": "idc",
            "is_choice": true,
            "choice_value": ["南汇", "欧阳路"],
            "attr_id": 1,
            "is_multivalue": false,
            "attr_alias": "IDC",
            "value_type": "text",
            "is_uniq": false
        }
    }
    ``` 
    
    * error 无
    

* GET `/api/v0.1/attributes/<string:attr_name>`、 `/api/v0.1/attributes/<int:attr_id>` 根据属性名称、别名或ID获取属性
    * param
        * `string:attr_name` 属性名称或别名
        * `int:attr_id` 属性ID
        * `attr_id`和`attr_name`选其一
    * return
    
    ```
    {
        "attribute": {
            "attr_name": "idc",
            "is_choice": true,
            "choice_value": ["南汇", "欧阳路"],
            "attr_id": 1,
            "is_multivalue": false,
            "attr_alias": "IDC",
            "value_type": "text",
            "is_uniq": false
        },
    }
    ```
    
    * error
        * `404` 找不到属性
        
* POST `/api/v0.1/attributes` 增加新的属性
    * param
         * `string:attr_name` 属性名称
         * `string:attr_alias` 属性别名，可为空，为空时等于`attr_name`
         * `boolean:choice_value` 若属性有预定义值, 则不能为空
         * `boolean:is_multivalue` 属性是否允许多值，默认`False`
         * `boolean:is_uniq` 属性是否唯一，默认`False`
         * `string:value_type` 属性值类型， `Enum("text", "int", "float", "date")`, 默认`text`
         
     * return
     
     ```
     {
         "attr_id":1
     }
     ```
     
     * error
         * `500` 属性已存在
         * `500` 属性增加失败
         
 * PUT `/api/v0.1/attributes/<int:attr_id>` 修改属性
    * param
         * `string:attr_name` 属性名称
         * `string:attr_alias` 属性别名，可为空，为空时等于`attr_name`
         * `boolean:choice_value` 若属性有预定义值, 则不能为空
         * `boolean:is_multivalue` 属性是否允许多值，值为0或者1，默认`False`
         * `boolean:is_uniq` 属性是否唯一，值为0或者1，默认`False`
         * `string:value_type` 属性值类型， `Enum("text", "int", "float", "date")`, 默认`text`
         
     * return
     
     ```
     {
         "attr_id":1
     }
     ```
     
     * error
         * `500` 属性已存在
         * `500` 属性增加失败
 
 * DELETE `/api/v0.1/attributes/<int:attr_id>` 根据ID删除属性
     * param
         * `int:attr_id` 属性ID
     * return
     
     ```
     {
         "message":"attribute %s deleted" % attr_name
     }
     ```
     
     * error
         * `404` 属性不存在
         * `500` 删除属性失败
 
#### CIType属性管理
 
 * GET `/api/v0.1/ci_types/<int:type_id>/attributes` 根据type_id查询固有属性列表
     * return
    
     ```
     {
        "attributes": [
            {
                "attr_name": "idc",
                "is_choice": true,
                "choice_value": ["南汇", "欧阳路"],
                "attr_id": 1,
                "is_multivalue": false,
                "attr_alias": "IDC",
                "value_type": "text",
                "is_uniq": false
            },
         ],
        "type_id": 1,
     }   
     ```
      
* POST `/api/v0.1/ci_types/<int:type_id>/attributes` 根据`attr_id`增加CIType的属性
    * param
        * `string:attr_id` `,`分隔的`attr_id`
        * `int:is_required` 0或者1
        
    * return
    
    ```
    {
        "attributes":[1, 2, 3]
    }
    ``` 
    
    * error
        * `404` CIType不存在
        * `404` 属性不存在
        * `500` 增加失败
        
* DELETE `/api/v0.1/ci_types/<int:type_id>/attributes` 删除CIType的属性
    * param
        * `string:attr_id` `,`分隔的`attr_id`
    
    * return
    
    ```
    {
        "attributes":[1, 2, 3]
    }
    ``` 
    
    * error
        * `404` CIType不存在
        * `404` 属性不存在
        * `500` 增加失败
        
        
### CIType管理接口

* `/api/v0.1/ci_types` 列出所有CI类型
    * param `string:type_name` 类型名称，允许为空
    * return
     
    ```
    {
     "numfound": 2,
     "ci_types": [
        {
            "uniq_key": "sn",
            "type_name": "物理机",
            "type_id": 1,
            "enabled": True,
            "icon_url": ""
        },
        {
            "uniq_key": "uuid",
            "type_name": "KVM",
            "type_id": 2,
            "enabled": True,
            "icon_url": ""
        }
     ],
    }
    ```
    * error 无
    
* GET `/api/v0.1/ci_types/query` 查询CI类型
    * param `string:q` 可以是type_id, type_name, type_alias
    * return
     
    ```
    {
      "citype": {
        "type_name": "software", 
        "type_id": 4, 
        "icon_url": "", 
        "type_alias": "\u8f6f\u4ef6", 
        "enabled": true, 
        "uniq_key": 21
      }
    }    
    ```
    * error 
        * `400` message=输入参数缺失
        * `404` message='citype is not found'
    
* POST `/api/v0.1/ci_types` 增加新CIType
    * param (下列参数任意一个或多个)
        * `string:type_name` CIType名称
        *  `string:type_alias` 类型别名，可为空
        * `int:_id` 唯一属性ID
        * `string:unique` 唯一属性名称         
        * `_id`和`unique`只能二选一
        * `icon_url`
        * `enabled` 0/1
    * return
    
    ```
    {
        "type_id": 2
    }
    ```
    
    * error
        * `400` message=输入参数缺失
        * `500` message=CIType已存在
        * `500` message=唯一属性不存在
        * `500` message=唯一属性不是唯一的 
               
* PUT `/api/v0.1/ci_types/<int:type_id>` 修改CIType
    * param (下列参数任意一个或多个)
        * `string:type_name` CIType名称
        *  `string:type_alias` 类型别名，可为空
        * `int:_id` 唯一属性ID
        * `string:unique` 唯一属性名称         
        * `_id`和`unique`只能二选一
        * `icon_url`
        * `enabled` 0/1
    * return
    
    ```
    {
        "type_id": 2
    }
    ```
    
    * error
        * `400` message=输入参数缺失
        * `500` message=CIType已存在
        * `500` message=唯一属性不存在
        * `500` message=唯一属性不是唯一的

* GET/POST `/api/v0.1/ci_types/<int:type_id>/enable` 修改CIType
    * param
        * `enabled` 0 or 1
    * return
    
    ```
    {
        "type_id": 2
    }
    ```
    
    * error
        * `500` 设置失败
        * `404` CIType不存在
        
* DELETE `/api/v0.1/ci_types/<int:type_id>` 根据ID删除CIType
    * return
    
    ```
    {
        "message":"ci type %s deleted" % type_name
    }
    ``` 
    * error
        * `500` 删除失败
        * `404` CIType不存在
        
### CITypeRelation管理接口

* GET `/api/v0.1/relation_types` 列出所有CIType关系类型名
    * return
          
    ```
    [
      {
        "created_at": null, 
        "deleted": false, 
        "deleted_at": null, 
        "id": 1, 
        "name": "contain", 
        "updated_at": null
      }
    ]
    ```
    * error 无
    
* GET `/api/v0.1/ci_type_relations/<int:parent_id>/children` 返回所有child id
    * return
     
    ```
    {
      "children": [
        {
          "ctr_id": 1,
          "type_name": "project", 
          "type_id": 2, 
          "icon_url": "", 
          "type_alias": "应用", 
          "enabled": true, 
          "uniq_key": 3
        }
      ]
    }    
    ```
    * error 无
    
* GET `/api/v0.1/ci_type_relations/<int:child_id>/parents` 返回parent id
    * return
     
    ```
    {
     "parents": [{'parent':1, 'relaltion_type': 'containes', "ctr_id":1}],
    }
    ```
    * error 无
    

* POST `/api/v0.1/ci_type_relations/<int:parent_id>/<int:child_id>` 增加CIType关系
    * param 
        * `string:relation_type` 类型名称
    * return
    
    ```
    {
        "ctr_id": 1
    }
    ``` 
    * error
        * `500` 增加失败
        * `404` CIType不存在
        
* DELETE `/api/v0.1/ci_type_relations/<int:ctr_id>` 根据`ctr_id`删除CIType关系
    * return
    
    ```
    {
        "message": "CIType relation deleted"
    }
    ``` 
    * error
        * `500` 删除失败
        * `404` 关系不存在
        


### CI管理接口

* GET `/api/v0.1/ci/type/<int:type_id>` 查询CIType的所有CI,一次返回25条记录
    * param 
        * `string:fields` 返回属性名、id，逗号隔开
        * `string:ret_key` 返回属性key,默认'name',还可是'id', 'alias'
        * `int:page` 页码
 
    * return
    
    ```  
    {
        "numfound": 1,
        "type_id":1,
        "page": 1,
        "cis": [
            {
              "ci_type": "KVM", 
              "_type": 1, 
              "nic": [
                    2
              ], 
              "hostname": "xxxxxx", 
          "_unique": "xxxxxx", 
          "_id": 1
            }
        ]
    }
    ```
    * error
        * `404` CIType不存在
        
* GET `/api/v0.1/ci/<int:ci_id>` 查询CI
 
    * return
    
    ```  
    {
        "ci": {
            "ci_type": "KVM", 
            "_type": 1, 
            "nic": [2], 
            "hostname": "xxxxx", 
            "_unique": "xxxxx", 
            "_id": 1
        }, 
        "ci_id": 1
    }
    ```
    * error 无
    
    
        
* POST `/api/v0.1/ci` 增加CI
    * param
        * `string:ci_type` CIType name 或者id
        * `string:_no_attribute_policy` 当添加不存在的attribute时的策略， 默认`ignore`
        * 其他url参数`k=v`： `k` 为属性名(id或别名亦可)， `v`为对应的值
        * 此CIType的`unique`字段必须包含在url参数中
    * return
    
    ```
    {
        "ci_id": 1,
    }
    ```
    * error
        * `500` 添加失败
        
* PUT `/api/v0.1/ci` 修改CI
    * param
        * `string:ci_type` CIType name 或者id
        * `string:_no_attribute_policy` 当添加不存在的attribute时的策略， 默认`ignore`
        * 其他url参数`k=v`： `k` 为属性名(id或别名亦可)， `v`为对应的值
        * 此CIType的`unique`字段必须包含在url参数中
    * return
    
    ```
    {
        "ci_id":1,
    }
    ```
    * error
        * `500` 添加失败
        
* DELETE `/api/v0.1/ci/<int:ci_id>` 删除ci
    * return
    
    ```
    {
        "message":"ok",
    }
    ```
    * error
        * `500` 删除失败
        
        
## CI Relation管理接口
    
* GET `/api/v0.1/ci_relations/<int:first_ci_id>/second_cis` 返回所有second cis
    * return
     
    ```
    {
      "numfound": 1, 
      "second_cis": [
        {
          "ci_type": "project", 
          "ci_type_alias": "应用", 
          "_type": 2, 
          "_id": 18, 
          "project_name": "cmdb-api"
        }
        ]
    } 
    ```
    * error 无
    
* GET `/api/v0.1/ci_relations/<int:second_ci_id>/first_cis` 返回first cis
    * return
     
    ```
    {
      "first_cis": [
        {
          "ci_type": "project", 
          "ci_type_alias": "应用", 
          "_type": 2, 
          "_id": 18, 
          "project_name": "cmdb-api"
        }
      ], 
      "numfound": 1
    }
    ```
    * error 无
    

* POST `/api/v0.1/ci_relations/<int:first_ci_id>/<int:second_ci_id>` 增加CI关系
    * param 
        * `int: more`  more实例
        * `string:relation_type` 类型名称
    * return
    
    ```
    {
        "cr_id":1
    }
    ``` 
    * error
        * `500` 增加失败
        * `404` CI不存在
        
* DELETE `/api/v0.1/ci_relations/<int:cr_id>` 根据`cr_id`删除CI关系
    * return
    
    ```
    {
        "message":"CIType relation deleted"
    }
    ``` 
    * error
        * `500` 删除失败
        * `404` 关系不存在
        
                
        
## 历史记录管理接口
* GET `/api/v0.1/history/records` 查询历史记录
    * param 
        * `int: page`  
        * `string: username` 变更用户
        * `string: start` 变更开始时间
        * `string: end` 变更结束时间
    * return
    
    ```
    {
      "username": "", 
      "start": "2014-12-31 14:57:43", 
      "end": "2015-01-07 14:57:43", 
      "records": [
        {
          "origin": null, 
          "attr_history": [], 
          "timestamp": "2015-01-01 22:12:39", 
          "reason": null, 
          "rel_history": {
            "add": 1
          }, 
          "user": 1, 
          "record_id": 1234, 
          "ticket_id": null
        }
        ]
    } 
    ``` 
    * error 无
        
 * GET `/api/v0.1/history/records/<int:record_id>` 历史记录详情
    * return
    
    ```
    {
      "username": "pycook",   
      "timestamp": "2015-01-02 20:21:16",
      "rel_history": {
        "add": [
          [
            123, 
            "deploy", 
            234
          ]
        ], 
        "delete": []
      }, 
      "attr_history": {}
    }
    ``` 
    
    * error
        * `404` 该记录不存在
