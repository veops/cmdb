/*
返回一个module对象

routes: []
stores: []
到时间都会插入到二级下面

会被插入到全局中
是否设置一个钩子呢？
插入前 调用的钩子？

*/
import genCmdbRoutes from './router'
import cmdbStore from './store'

export default {
    name: 'cmdb',
    route: genCmdbRoutes,
    store: cmdbStore
}
