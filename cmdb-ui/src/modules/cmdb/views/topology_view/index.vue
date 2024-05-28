<template>
  <div class="topo-wrap" :style="{ height: `${windowHeight - 96}px` }" @click="closeNodeTips">
    <div v-if="!topoGroups.length" class="topo-empty">
      <a-empty :image="emptyImage" description=""></a-empty>
      <a-button
        icon="plus"
        size="small"
        type="primary"
        @click="handleClickAddGroup">{{ $t('cmdb.ciType.addGroup') }}</a-button>
    </div>
    <SplitPane
      v-else
      :min="180"
      :max="300"
      :paneLengthPixel.sync="paneLengthPixel"
      appName="cmdb-topo-views"
      :triggerLength="18"
    >
      <template #one>
        <a-input
          :placeholder="$t('cmdb.topo.searchPlaceholder')"
          class="cmdb-topo-left-input"
          @pressEnter="handleSearch"
        >
          <a-icon slot="prefix" type="search" />
        </a-input>
        <div class="topo-left">
          <div class="topo-left-title">
            <a-button
              type="primary"
              size="small"
              ghost
              @click="handleClickAddGroup"
              class="ops-button-ghost"
            ><ops-icon type="veops-increase" />{{ $t('cmdb.ciType.group') }}</a-button
            >
          </div>
          <draggable class="topo-left-content" :list="computedTopoGroups" @end="handleChangeGroups" filter=".undraggable">
            <div v-for="group in computedTopoGroups" :key="group.id || group.name">
              <div
                :class="
                  `${currentGId === group.id && !currentCId ? 'selected' : ''} topo-left-group ${
                    group.id === undefined ? 'undraggable' : ''
                  }`
                "
                @click="handleClickGroup(group.id)"
              >
                <div>
                  <OpsMoveIcon
                    v-if="group.id"
                    style="width: 17px; height: 17px; display: none; position: absolute; left: -3px; top: 10px"
                  />
                  <span style="font-weight: 700">{{ group.name || $t('other') }}</span>
                  <span :style="{ color: '#c3cdd7' }">({{ group.views.length }})</span>
                </div>
                <a-space>
                  <a-tooltip>
                    <template slot="title">{{ $t('cmdb.topo.addTopoViewInGroup') }}</template>
                    <a><ops-icon type="veops-increase" @click="handleCreate(group)"/></a>
                  </a-tooltip>
                  <template v-if="group.id">
                    <a-tooltip >
                      <template slot="title">{{ $t('cmdb.ciType.editGroup') }}</template>
                      <a><a-icon type="edit" @click="handleEditGroup(group)"/></a>
                    </a-tooltip>
                    <a-tooltip>
                      <template slot="title">{{ $t('cmdb.ciType.deleteGroup') }}</template>
                      <a :style="{color: 'red'}"><a-icon type="delete" @click="handleDeleteGroup(group)"/></a>
                    </a-tooltip>
                  </template>
                </a-space>
              </div>
              <draggable
                v-model="group.views"
                group="topo"
                :animation="100"
                @start="start(group)"
                @end="end(group)"
                @add="add(group)"
                filter=".undraggable"
              >
                <div
                  v-for="topo in group.views"
                  :key="topo.id"
                  :class="`${currentCId === topo.id ? 'selected' : ''} topo-left-detail`"
                  @click="handleClickView(group.id, topo.id, topo.name)"
                >
                  <div :class="`${ group.id === undefined ? 'undraggable' : '' }`">
                    <OpsMoveIcon
                      v-if="group.id"
                      style="width: 17px; height: 17px; display: none; position: absolute; left: -1px; top: 8px"
                    />
                    <span class="topo-left-detail-icon">
                      <template v-if="topo.icon">
                        <img
                          v-if="topo.icon.split('$$')[2]"
                          :src="`/api/common-setting/v1/file/${topo.icon.split('$$')[3]}`"
                        />
                        <ops-icon
                          v-else
                          :style="{
                            color: topo.icon.split('$$')[1],
                            fontSize: '14px',
                          }"
                          :type="topo.icon.split('$$')[0]"
                        />
                      </template>
                      <span :style="{ color: '#2f54eb' }" v-else>{{ topo.name[0].toUpperCase() }}</span>
                    </span>
                  </div>
                  <span class="topo-left-detail-title">{{ topo.alias || topo.name }}</span>
                  <a-dropdown>
                    <a class="topo-left-detail-action">
                      <ops-icon type="veops-more" />
                    </a>
                    <a-menu slot="overlay">
                      <a-menu-item @click="(e) => handlePerm(e, topo)">
                        <a-icon type="user-add" />
                        {{ $t('grant') }}
                      </a-menu-item>
                      <a-menu-item @click="(e) => handleEdit(e, topo)">
                        <a-icon type="edit" />
                        {{ $t('cmdb.topo.edit') }}
                      </a-menu-item>
                      <a-menu-item @click="(e) => handleDelete(e, topo)">
                        <a-icon type="delete" />
                        {{ $t('cmdb.topo.delete') }}
                      </a-menu-item>
                    </a-menu>
                  </a-dropdown>
                </div>
              </draggable>
            </div>
          </draggable>
        </div>
      </template>
      <template #two>
        <div class="topo-right">
          <div v-if="currentCId">
            <div :style="{ height: `${windowHeight - 80}px` }" ref="rightTopoView">
              <RelationGraph ref="showTopoView" :options="graphOptions2" :on-node-click="showNodeTips">
                <template #node="{node}">
                  <div :style="{ lineHeight: '20px' }">
                    <ops-icon type="caise-wuliji" />
                    <span :style="{ marginLeft: '5px', textOverflow: 'ellipsis' }">{{ node.text }}aaa</span>
                  </div>
                </template>
                <template #graph-plug>
                  <div v-if="(isShowNodeTipsPanel && currentNodeValues && currentNodeAttributes.length) || errorMessageShow" :style="nodeTipsPosition" class="node-tips">
                    <a-descriptions
                      v-if="currentNodeValues"
                      bordered
                      size="small"
                      :column="{ xxl: 1, xl: 1, lg: 1, md: 1, sm: 1, xs: 1 }"
                    >
                      <a-descriptions-item :label="attr.alias" v-for="attr in currentNodeAttributes" :key="attr.name">
                        {{ currentNodeValues[attr.name] }}
                      </a-descriptions-item>
                    </a-descriptions>
                    <span v-if="errorMessageShow" style="color: red">{{ errorMessage }}</span>
                  </div>
                </template>
              </RelationGraph>
            </div>
          </div>
          <div v-else class="topo-right-empty">
            <a-empty :image="emptyImage" description=""></a-empty>
            <a-button icon="plus" size="small" type="primary" :disabled="!permissions.includes('admin') && !permissions.includes('cmdb_admin')" @click="handleCreateViewFromEmpty">{{
              $t('cmdb.topo.addTopoView')
            }}</a-button>
          </div>
        </div>
      </template>
    </SplitPane>
    <a-modal v-model="modalVisible" :title="modalTitle" @ok="handleSubmitEditGroup">
      <a-form-item :label="$t('name')" :label-col="{ span: 4 }" :wrapper-col="{ span: 16 }">
        <a-input v-model="editingInput" />
      </a-form-item>
    </a-modal>
    <CustomDrawer
      :closable="false"
      :title="drawerTitle"
      :visible="drawerVisible"
      @close="onClose"
      placement="right"
      width="900px"
      :destroyOnClose="true"
      :bodyStyle="{ height: 'calc(100vh - 108px)' }"
    >
      <a-form
        :form="form"
        :layout="formLayout"
        :label-col="formItemLayout.labelCol"
        :wrapper-col="formItemLayout.wrapperCol"
      >
        <a-form-item :label="$t('cmdb.topo.viewName')">
          <a-input
            name="name"
            :placeholder="$t('cmdb.topo.viewNamePlaceholder')"
            v-decorator="[
              'name',
              {
                rules: [
                  { required: true, message: $t('cmdb.topo.inputNameTips') },
                  {
                    message: $t('cmdb.topo.inputNameTips'),
                  },
                ],
              },
            ]"
          />
        </a-form-item>
        <a-form-item :label="$t('cmdb.topo.centralNodeType')" prop="central_node_type">
          <a-select @change="CITypeChange" v-decorator="['central_node_type', { rules: [{ required: true, message: $t('cmdb.topo.typeRequired') }]}]" :showSearch="true" optionFilterProp="label">
            <a-select-option v-for="t in ciTypes" :key="t.id" :value="t.id" :label="t.alias">{{ t.alias }}</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item :label="$t('cmdb.topo.filterInstances')" prop="central_node_instances">
          <a-input
            v-decorator="['central_node_instances', { rules: [{ required: true, message: $t('cmdb.topo.instancesRequired') }]}]"
            :placeholder="$t('cmdb.ciType.selectFromCMDBTips')"
          >
            <a @click="handleOpenCmdb" slot="suffix"><a-icon type="menu"/></a>
          </a-input>
        </a-form-item>
        <a-form-item :label="$t('cmdb.topo.path')" prop="path">
          <div :style="{ height: '250px', border: '1px solid #e4e7ed' }">
            <SeeksRelationGraph ref="ciTypeRelationGraph" :options="graphOptions">
              <div slot="node" slot-scope="{ node }" :style="{ lineHeight: '20px' }">
                <a-checkbox
                  :checked="checkedNodes.includes(node.id)"
                  @change="(e) => checked(e, node)"
                ></a-checkbox>
                <span :style="{ marginLeft: '5px' }">{{ node.text }}</span>
              </div>
            </SeeksRelationGraph>
          </div>
        </a-form-item>
        <a-form-item :style="{ display: 'none' }" :label="$t('cmdb.topo.aggregationCount')" prop="aggregation_count" :help="$t('cmdb.topo.aggreationCountTip')">
          <a-input-number
            :style="{ width: '100%' }"
            v-decorator="['aggregation_count']"
          >
            <a @click="handleOpenCmdb" slot="suffix"><a-icon type="menu"/></a>
          </a-input-number>
        </a-form-item>
        <div :class="{ 'chart-left-preview': true, 'chart-left-preview-empty': !isShowPreview }">
          <span
            class="chart-left-preview-operation"
            :style="{zIndex: '800'}"
            @click="showPreview"
          ><a-icon type="play-circle" /> {{ $t('cmdb.custom_dashboard.preview') }}</span
          >
          <template v-if="isShowPreview">
            <RelationGraph ref="previewTopoView" :options="graphOptionsPrivew">
              <div slot="node" slot-scope="{ node }" :style="{ lineHeight: '20px' }">
                <span :style="{ marginLeft: '5px' }">{{ node.text }}</span>
              </div>
            </RelationGraph>
          </template>
        </div>
        <a-form-item>
          <a-input name="id" type="hidden" v-decorator="['id', { rules: [] }]" />
        </a-form-item>
        <div class="custom-drawer-bottom-action">
          <a-button @click="handleSubmit" :loading="loading" type="primary" style="margin-right: 1rem">{{
            $t('confirm')
          }}</a-button>
          <a-button @click="onClose">{{ $t('cancel') }}</a-button>
        </div>
      </a-form>
      <CMDBExprDrawer ref="cmdbDrawer" type="resourceView" :typeId="CITypeId" @copySuccess="copySuccess" />
    </CustomDrawer>
    <CMDBGrant ref="cmdbGrant" resourceType="TopologyView" app_id="cmdb" />
  </div>
</template>
<script>
import _ from 'lodash'
import draggable from 'vuedraggable'
import emptyImage from '@/assets/data_empty.png'
import SplitPane from '@/components/SplitPane'
import { ops_move_icon as OpsMoveIcon } from '@/core/icons'
import { getCITypeGroups } from '@/modules/cmdb/api/ciTypeGroup'
import { roleHasPermissionToGrant } from '@/modules/acl/api/permission'
import { searchResourceType } from '@/modules/acl/api/resource'
import SeeksRelationGraph from '@/modules/cmdb/3rd/relation-graph'
import RelationGraph from 'relation-graph'
import CMDBGrant from '@/modules/cmdb/components/cmdbGrant'
import { getSubscribeAttributes } from '@/modules/cmdb/api/preference'
import { searchCI } from '@/modules/cmdb/api/ci'
import { getTopoGroups, postTopoGroup, putTopoGroupByGId, putTopoGroupsOrder, deleteTopoGroup, getTopoView, addTopoView, updateTopoView, deleteTopoView, getRelationsByTypeId, previewTopoView, showTopoView } from '@/modules/cmdb/api/topology'
import CMDBExprDrawer from '@/components/CMDBExprDrawer'

const currentTopoKey = 'ops_cmdb_topo_currentId'
export default {
  name: 'TopologyView',
  components: {
    draggable,
    OpsMoveIcon,
    SplitPane,
    CMDBExprDrawer,
    SeeksRelationGraph,
    RelationGraph,
    CMDBGrant,
  },
  data() {
    const defaultOptions = {
      debug: false,
      allowShowMiniToolBar: true,
      allowShowMiniNameFilter: true,
      defaultFocusRootNode: false,
    }
    const graphOptions = {
      ...defaultOptions,
      allowShowMiniToolBar: false,
      allowShowMiniNameFilter: false,
      defaultNodeColor: 'rgba(230, 247, 255, 1)',
      defaultNodeFontColor: 'rgba(33, 32, 32, 1)',
      layouts: [
        {
          layoutName: 'tree',
          layoutClassName: 'seeks-layout-center',
        },
      ],
    }
    const graphOptions2 = {
      // ...defaultOptions,
      backgrounImageNoRepeat: true,
      placeOtherGroup: true,
      moveToCenterWhenRefresh: true,
      zoomToFitWhenRefresh: true,
      useAnimationWhenExpanded: false,
      defaultNodeShape: 1,
      defaultLineShape: 4,
      defaultNodeBorderWidth: 0,
      defaultNodeWidth: 150,
      defaultNodeHeight: 30,
      min_per_width: undefined,
      max_per_width: 200,
      min_per_height: 40,
      max_per_height: undefined,
      defaultLineColor: '#CACDD9',
      defaultNodeColor: '#29AAE1',
      defaultNodeFontColor: '#ffffff',
      defaultNodeBorderColor: '#b1c9ff',
      defaultExpandHolderPosition: 'right',
      defaultJunctionPoint: 'lr',
      layouts: [
        {
          layoutName: 'tree',
          from: 'left',
          layoutClassName: 'seeks-layout-center',
          defaultExpandHolderPosition: 'hide',
          defaultJunctionPoint: 'border',
        },
      ],
    }
    const graphOptionsPrivew = {
      ...graphOptions2,
      toolBarDirection: 'h',
      toolBarPositionH: 'left',
      toolBarPositionV: 'top',
    }
    return {
      graphOptions,
      graphOptions2,
      graphOptionsPrivew,
      emptyImage,
      paneLengthPixel: 250,
      loading: false,
      searchValue: '',

      currentId: null,
      topoGroups: [],
      CITypeId: null,
      ciTypes: [],

      startId: null,
      endId: null,
      addId: null,
      addGroup: null,
      startGroup: null,

      view: null,

      modalTitle: this.$t('cmdb.ciType.addGroup'),
      modalVisible: false,
      editingGroup: null,
      editingInput: '',

      resource_type: {},

      form: this.$form.createForm(this),
      drawerVisible: false,
      drawerTitle: '',
      selectGroup: {}, // add view in group

      formLayout: 'horizontal',
      isShowPreview: false,

      checkedNodes: [],
      nodes: [],

      currentNode: {},
      currentNodeAttributes: [],
      currentNodeValues: {},
      currentNodes: [],
      graphJsonData: null,
      isShowNodeTipsPanel: false,
      nodeTipsPosition: {},

      errorMessageShow: false,
      errorMessage: '',
    }
  },
  provide() {
    return {
      resource_type: () => {
        return this.resource_type
      },
    }
  },
  mounted() {
    searchResourceType({ page_size: 9999, app_id: 'cmdb' }).then((res) => {
      this.resource_type = { groups: res.groups, id2perms: res.id2perms }
    })
    const _currentId = localStorage.getItem(currentTopoKey)
    if (_currentId) {
      this.currentId = _currentId
    }
    this.loadTopoViews(!_currentId)
    let ciTypes = []
    getCITypeGroups({ need_other: true }).then((res) => {
      res.forEach((item) => {
        if (item.ci_types && item.ci_types.length) {
          ciTypes = ciTypes.concat(item.ci_types)
        }
      })
      this.ciTypes = ciTypes
    })
    this.showTopoView(this.currentId.split('%')[1])
  },
  computed: {
    windowHeight() {
      return this.$store.state.windowHeight
    },
    windowWidth() {
      return this.$store.state.windowWidth
    },
    permissions() {
      return this.$store.state.user?.roles?.permissions || []
    },
    currentGId() {
      if (this.currentId) {
        return Number(this.currentId.split('%')[0])
      }
      return null
    },
    currentCId() {
      if (this.currentId) {
        if (this.currentId.split('%')[1] !== 'null') {
          return Number(this.currentId.split('%')[1])
        }
        return null
      }
      return null
    },
    computedTopoGroups() {
      if (this.searchValue) {
        const groups = _.cloneDeep(this.topoGroups)
        groups.forEach((item) => {
          item.views = item.views.filter((_item) => _item.name.toLowerCase().includes(this.searchValue.toLowerCase()))
        })
        return groups
      }
      return this.topoGroups
    },
    formItemLayout() {
      const { formLayout } = this
      return formLayout === 'horizontal'
        ? {
            labelCol: { span: 5 },
            wrapperCol: { span: 16 },
          }
        : {}
    },
  },
  methods: {
    closeNodeTips(e) {
      e.preventDefault()
      e.stopPropagation()
      console.log('close node tips')
      if (e.target && e.target.innerHTML.includes(this.currentNode.text)) {
        return
      }
      if (this.isShowNodeTipsPanel === true) {
        this.isShowNodeTipsPanel = false
      }
      if (this.errorMessageShow === true) {
        this.errorMessageShow = false
      }
    },
    handleClickAddGroup() {
      this.editingGroup = {}
      this.editingInput = ''
      this.modalTitle = this.$t('cmdb.ciType.addGroup')
      this.modalVisible = true
    },
    handleClickGroup(gId) {
      this.currentId = null
      this.$nextTick(() => {
        this.currentId = `${gId}%null%null`
        localStorage.setItem(currentTopoKey, this.currentId)
      })
    },
    handleClickView(gId, viewId, viewName) {
      this.currentId = null
      this.$nextTick(() => {
        this.currentId = `${gId}%${viewId}%${viewName}`
        localStorage.setItem(currentTopoKey, this.currentId)
        this.showTopoView(viewId)
      })
    },
    handleEditGroup(g) {
      this.editingGroup = g
      this.editingInput = g.name
      this.modalTitle = this.$t('cmdb.ciType.editGroup')
      this.modalVisible = true
    },
    async handleDeleteGroup(g) {
      if (g.views && g.views.length > 0) {
        this.$message.error(this.$t('cmdb.ciType.cannotDeleteGroupTips'))
        return
      }
      const that = this
      this.$confirm({
        title: that.$t('warning'),
        content: that.$t('cmdb.ciType.confirmDeleteGroup', { groupName: `${g.name}` }),
        onOk() {
          deleteTopoGroup(g.id).then((res) => {
            that.$message.success(that.$t('deleteSuccess'))
            that.loadTopoViews(true)
          })
        },
      })
    },
    handleChangeGroups() {
      putTopoGroupsOrder({ group_ids: this.topoGroups.filter((c) => c.id).map((c) => c.id) })
      .then(() => {
        this.$message.success(this.$t('saveSuccess'))
      })
      .catch(() => {
        this.loadTopoViews(!this.currentId)
      })
    },
    start(g) {
      console.log('start', g)
      this.startId = g.id
    },
    end(g) {
      console.log('end', g)
      this.endId = g.id
      const that = this
      let groupId = null
      const payload = {}
      if (this.startId === g.id && g.id && this.addId) {
        // change from one group to another
        console.log(this.addGroup)
        console.log(this.addId)
        groupId = this.addGroup.id
        payload.name = this.addGroup.name
        payload.view_ids = this.addGroup.views.map(i => i.id)
      }
      if (this.startId === g.id && g.id && !this.addId) {
        // Change order within group
        groupId = g.id
        payload.name = g.name
        payload.view_ids = g.views.map(i => i.id)
      }
      if (groupId) {
        putTopoGroupByGId(groupId, { view_ids: g.views.map((i) => i.id) })
        .then(() => {
          this.$message.success(that.$t('saveSuccess'))
        })
        .catch(() => {
          this.loadTopoViews(!this.currentId)
        })
        .finally(() => {
          this.startId = null
          this.endId = null
          this.addId = null
        })
      }
    },
    add(g) {
      console.log('add', g.name)
      this.addId = g.id
      this.addGroup = _.cloneDeep(g)
    },
    async loadTopoViews(isResetCurrentId = false) {
      const groups = await getTopoGroups()
      let alreadyReset = false
      if (isResetCurrentId) {
        this.currentId = null
      }
      this.$nextTick(() => {
        groups.forEach((g) => {
          if (isResetCurrentId && !alreadyReset && g.views && g.views.length) {
            this.currentId = `${g.id}%${g.views[0].id}%${g.views[0].name}`
            alreadyReset = true
          }
          if (!g.views) {
            g.views = []
          }
        })
        this.topoGroups = groups
        localStorage.setItem(currentTopoKey, this.currentId)
      })
    },
    async handleSubmitEditGroup() {
      if (this.editingGroup && this.editingGroup.id) {
        await putTopoGroupByGId(this.editingGroup.id, {
          name: this.editingInput,
          view_ids: this.editingGroup.views.map((i) => i.id),
        })
        this.$message.success(this.$t('updateSuccess'))
      } else {
        const { id } = await postTopoGroup({ name: this.editingInput })
        this.currentId = `${id}%null%null`
        this.$message.success(this.$t('addSuccess'))
      }
      this.modalVisible = false
      this.loadTopoViews()
    },
    handleSearch(e) {
      this.searchValue = e.target.value
    },
    handleCreate(g) {
      this.drawerTitle = this.$t('cmdb.topo.addTopoView')
      this.drawerVisible = true
      this.selectGroup = g
    },
    handleCreateViewFromEmpty() {
      this.drawerTitle = this.$t('cmdb.topo.addTopoView')
      this.drawerVisible = true
      const _find = this.topoGroups.find((item) => item.id === this.currentGId)
      this.selectGroup = _find
    },
    async handleSubmit(e) {
      e.preventDefault()
      this.form.validateFields(async (err, values) => {
        if (!err) {
          const { name, central_node_type, central_node_instances, aggregation_count } = values
          const payload = { name, central_node_type, central_node_instances }
          if (aggregation_count) {
            payload.option = { aggregation_count }
          } else {
            payload.option = {}
          }
          if (this.selectGroup && this.selectGroup.id) {
            payload.group_id = this.selectGroup.id
          }
          payload.path = this.wrapPath()
          this.loading = true
          if (values.id) {
            await updateTopoView(values.id, payload).then(res => {
              const { id } = res
              this.currentId = `${this.selectGroup?.id || ''}%${id}%${payload.name}`
              this.showTopoView(id)
            })
          } else {
            if (!payload.group_id) {
              this.$message.error(this.$t('cmdb.topo.groupRequired'))
              this.loading = false
              return
            }
            await addTopoView(payload).then(res => {
              const { id } = res
              this.currentId = `${this.selectGroup?.id || ''}%${id}%${payload.name}`
              this.showTopoView(id)
            })
          }
          localStorage.setItem(currentTopoKey, this.currentId)
          setTimeout(() => {
            this.loadTopoViews()
          }, 2000)
          this.drawerVisible = false
        }
      })
      this.loading = false
    },
    wrapPath() {
      const path = {}
      this.checkedNodes.forEach(nodeId => {
        const _nodes = this.nodes.filter(i => String(i.id) === nodeId)
        _nodes.forEach(_node => {
          const levels = _node.level || [0]
          levels.forEach(level => {
            if (level in path) {
              path[level].push(nodeId)
            } else {
              path[level] = [nodeId]
            }
          })
        })
      })
      return path
    },
    onClose() {
      this.form.resetFields()
      this.drawerVisible = false
    },
    showPreview() {
      console.log('click show preview')
      this.isShowPreview = true
      this.form.validateFields(async (err, values) => {
        if (!err) {
          const payload = {
            central_node_type: values.central_node_type,
            central_node_instances: values.central_node_instances,
            path: this.wrapPath() }
          previewTopoView(payload).then(res => {
            const nodes = []
            const links = []
            res.links.forEach(item => {
              links.push({
                from: `${item.from}`,
                to: `${item.to}`,
                disableDefaultClickEffect: true,
              })
            })
            res.nodes.forEach(item => {
              nodes.push({
                id: `${item.id}`,
                text: item.name,
                nodeShape: 1,
                borderWidth: -1,
                disableDefaultClickEffect: true,
              })
            })
            const _graphJsonData = {
              nodes,
              links,
            }
            if (!nodes.length) {
              this.$message.error(this.$t('cmdb.topo.noData'))
              return
            }
            this.$refs.previewTopoView.setJsonData(_graphJsonData, (res) => {
            })
          })
        }
      })
    },
    showTopoView(viewId) {
      if (viewId === 'null' || !viewId) {
        return
      }
      showTopoView(viewId).then(res => {
        const nodes = []
        const links = []
        this.currentNodes = res.nodes
        res.links.forEach(item => {
          links.push({
            from: `${item.from}`,
            to: `${item.to}`,
            // text: `${item.text}`,
            disableDefaultClickEffect: false,
          })
        })
        res.nodes.forEach(item => {
          nodes.push({
            id: `${item.id}`,
            text: item.name,
            data: {},
          })
        })
        const _graphJsonData = {
          nodes,
          links,
        }
        if (!nodes.length) {
          this.$message.error(this.$t('cmdb.topo.noData'))
          return
        }
        // this.$nextTick(() => {
        this.$refs.showTopoView.setJsonData(_graphJsonData)
        // })
      })
    },
    handleOpenCmdb() {
      this.$refs.cmdbDrawer.open()
    },
    copySuccess(text) {
      this.form.setFieldsValue({ 'central_node_instances': `${text}` })
    },
    async CITypeChange(value) {
      this.CITypeId = value
      this.form.setFieldsValue({
        central_node_instances: ''
      })
      this.checkedNodes = [String(value)]
      this.getRelationsByTypeId(value)
      if (this.$refs.cmdbDrawer.$refs.resourceSearch) {
        this.$refs.cmdbDrawer.$refs.resourceSearch.typeId = value
        await this.$refs.cmdbDrawer.$refs.resourceSearch.getCIType(value)
        await this.$refs.cmdbDrawer.$refs.resourceSearch.getAttrsByType(value)
        this.$refs.cmdbDrawer.$refs.resourceSearch.$refs['search'].currenCiType = [value]
        this.$refs.cmdbDrawer.$refs.resourceSearch.loadInstance()
      }
    },
    handlePerm(e, v) {
      e.domEvent.preventDefault()
      e.domEvent.stopPropagation()
      roleHasPermissionToGrant({
        app_id: 'cmdb',
        resource_type_name: 'TopologyView',
        perm: 'grant',
        resource_name: v.name,
      }).then((res) => {
        if (res.result) {
          this.$refs.cmdbGrant.open({ name: v.name, cmdbGrantType: 'TopologyView', CITypeId: v.id })
        } else {
          this.$message.error(this.$t('noPermission'))
        }
      })
    },
    async handleEdit(e, record) {
      e.domEvent.preventDefault()
      e.domEvent.stopPropagation()
      this.drawerTitle = this.$t('cmdb.topo.editTopoView')
      this.drawerVisible = true
      await getTopoView(record.id).then((res) => {
        this.editView = res ?? null
      })
      this.$nextTick(() => {
        this.form.setFieldsValue({
          id: record.id,
          name: record.name,
          central_node_type: record.central_node_type,
          central_node_instances: record.central_node_instances,
          aggregation_count: record.option?.aggregation_count
        })
      })
      const checkedNodes = []
      Object.values(record.path).forEach(item => {
        checkedNodes.push(...item)
      })
      this.checkedNodes = Array.from(new Set(checkedNodes))
      await this.getRelationsByTypeId(record.central_node_type)
      this.CITypeId = record.central_node_type
      this.getRelationsByTypeId(record.central_node_type)
      if (this.$refs.cmdbDrawer.$refs.resourceSearch) {
        this.$refs.cmdbDrawer.$refs.resourceSearch.typeId = record.central_node_type
        await this.$refs.cmdbDrawer.$refs.resourceSearch.getCIType(record.central_node_type)
        await this.$refs.cmdbDrawer.$refs.resourceSearch.getAttrsByType(record.central_node_type)
        this.$refs.cmdbDrawer.$refs.resourceSearch.$refs['search'].currenCiType = [record.central_node_type]
        this.$refs.cmdbDrawer.$refs.resourceSearch.loadInstance()
      }
    },
    handleDelete(e, record) {
      e.domEvent.preventDefault()
      e.domEvent.stopPropagation()
      const that = this
      this.$confirm({
        title: that.$t('warning'),
        content: that.$t('cmdb.topo.confirmDeleteView', { viewName: `${record.name}` }),
        onOk() {
          deleteTopoView(record.id).then((res) => {
            that.$message.success(that.$t('deleteSuccess'))
            that.loadTopoViews(true)
          })
        },
      })
    },
    async getRelationsByTypeId(typeId) {
      getRelationsByTypeId(typeId).then(res => {
        const nodes = []
        const links = []
        this.nodes = res.nodes
        res.edges.forEach(item => {
          links.push({
            from: `${item.from_id}`,
            to: `${item.to_id}`,
            text: `${item.text}`,
            disableDefaultClickEffect: true,
          })
        })
        res.nodes.forEach(item => {
          nodes.push({
            id: `${item.id}`,
            name: item.alias || item.name,
            nodeShape: 1,
            borderWidth: -1,
            disableDefaultClickEffect: true,
          })
        })
        const _graphJsonData = {
          rootId: `${typeId}`,
          nodes,
          links,
        }
        this.graphJsonData = _graphJsonData
        if (!nodes.length) {
          this.$message.error(this.$t('cmdb.topo.noData'))
          return
        }
        this.$nextTick(() => {
          this.$refs.ciTypeRelationGraph.setJsonData(_graphJsonData, (res) => {
          })
        })
      })
    },
    checked(e, node) {
      if (e.target.checked) {
        if (this.checkedNodes.findIndex(i => i === node.id) === -1) {
          this.checkedNodes.push(node.id)
        }
      } else {
        this.checkedNodes.splice(this.checkedNodes.findIndex(i => i === node.id), 1)
      }
    },
    async showNodeTips(nodeObject, $event) {
      console.log('node click')
      $event.preventDefault()
      $event.stopPropagation()
      const _base_position = this.$refs.showTopoView.getInstance().options.fullscreen ? { x: 0, y: 0 } : this.$refs.rightTopoView.getBoundingClientRect()
      if (this.currentNode !== nodeObject) {
        this.currentNodeValues = null
        this.errorMessageShow = false
        this.currentNode = nodeObject
        const rawNode = this.currentNodes.find(item => item.id === nodeObject.id)
        if (rawNode) {
          const [ attributes ] = await Promise.all([getSubscribeAttributes(rawNode.type_id)])
          this.currentNodeAttributes = attributes?.attributes || []
          if (!this.currentNodeAttributes.length) {
            this.errorMessage = this.$t('cmdb.topo.noPreferenceAttributes')
            this.errorMessageShow = true
            this.currentNodeValues = null
            this.isShowNodeTipsPanel = false
          }
          await searchCI({ q: `_id:${rawNode.id}` }, false).then(res => {
            if (!res.result.length) {
              this.errorMessage = this.$t('cmdb.topo.noInstancePerm')
              this.errorMessageShow = true
              this.currentNodeValues = null
              this.isShowNodeTipsPanel = false
            } else {
              this.currentNodeValues = res.result[0]
            }
          }).catch(error => {
            this.errorMessage = ((error.response || {}).data || {}).message
            this.errorMessageShow = true
            this.currentNodeValues = null
            this.isShowNodeTipsPanel = false
          })
        }
      }
      this.nodeTipsPosition = {}
      if (this.windowWidth - $event.clientX < (this.windowWidth - _base_position.x) / 2) {
        this.nodeTipsPosition.right = this.windowWidth - $event.clientX - 20 + 'px'
      } else {
        this.nodeTipsPosition.left = $event.clientX - _base_position.x - $event.offsetX - 20 + 'px'
      }
      if (this.windowHeight - $event.clientY < this.windowHeight / 2) {
        this.nodeTipsPosition.bottom = this.windowHeight - $event.clientY + $event.offsetY + 'px'
      } else {
        this.nodeTipsPosition.top = $event.clientY - _base_position.y + 30 - $event.offsetY + 'px'
      }
      this.nodeTipsPosition.maxHeight = this.windowHeight / 2 - 100 + 'px'
      this.isShowNodeTipsPanel = true
      console.log(this.nodeTipsPosition)
    },
    hideNodeTips(nodeObject, $event) {
      this.isShowNodeTipsPanel = false
    },
  },
}
</script>

<style lang="less" scoped>
.ant-message {
  z-index: 99999999 !important;
}
.topo-wrap {
  margin: 0 0 -24px 0;
  .topo-empty {
    position: absolute;
    text-align: center;
    left: 50%;
    top: 40%;
    transform: translate(-50%, -50%);
  }

  .topo-left {
    width: 100%;
    overflow: auto;
    float: left;

    .topo-left-content {
      max-height: calc(100% - 45px);
      overflow: hidden;
      &:hover {
        overflow: auto;
      }
    }
    .topo-left-title {
      padding: 10px 0;
      display: flex;
      flex-direction: row;
      justify-content: space-between;
      color: @text-color_3;
    }
    .topo-left-group {
      position: relative;
      padding: 8px 0 8px 14px;
      color: rgb(99, 99, 99);
      cursor: pointer;
      font-size: 14px;
      display: flex;
      flex-direction: row;
      justify-content: space-between;
      align-items: center;
      > div:nth-child(2) {
        font-size: 14px;
        display: none;
      }
      &:hover {
        background-color: @primary-color_3;
        > div:nth-child(2) {
          display: inline-flex;
        }
        svg {
          display: inline !important;
        }
      }
    }
    .topo-left-detail {
      padding: 3px 14px;
      cursor: pointer;
      position: relative;
      display: flex;
      flex-direction: row;
      justify-content: flex-start;
      align-items: center;
      margin-bottom: 4px;
      height: 32px;
      line-height: 32px;
      .topo-left-detail-action {
        display: none;
        margin-left: auto;
      }
      .topo-left-detail-title {
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;
      }
      .topo-left-detail-icon {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 20px;
        height: 20px;
        border-radius: 2px;
        box-shadow: 0px 1px 2px rgba(47, 84, 235, 0.2);
        margin-right: 6px;
        background-color: #fff;
        img {
          max-height: 20px;
          max-width: 20px;
        }
      }
      &:hover {
        background-color: @primary-color_3;
        svg {
          display: inline !important;
        }
        .topo-left-detail-action {
          display: inline-flex;
        }
      }
    }
    .selected {
      background-color: @primary-color_3;
      .topo-left-detail-title {
        font-weight: 700;
      }
    }
  }
  .topo-right {
    width: 100%;
    position: relative;
    background-color: #fff;
    .topo-right-empty {
      position: absolute;
      text-align: center;
      left: 50%;
      top: 40%;
      transform: translate(-50%, -50%);
    }
  }
  .topo-left,
  .topo-right {
    height: 100%;
  }
  .node-tips {
    z-index: 999;
    padding: 10px;
    background-color: #ffffff;
    border:#eeeeee solid 1px;
    box-shadow: 0px 0px 8px #cccccc;
    position: absolute;
    overflow: auto;
  }
}
.chart-left-preview {
  border: 1px solid #e4e7ed;
  border-radius: 2px;
  height: 280px;
  width: 92%;
  position: relative;
  padding: 12px;
  .chart-left-preview-operation {
    color: #86909c;
    position: absolute;
    top: 12px;
    right: 12px;
    cursor: pointer;
  }
  .chart-left-preview-box {
    padding: 6px 12px;
    height: 250px;
    border-radius: 8px;
  }
}
</style>

<style lang="less">
.cmdb-topo-left-input {
  input {
    background-color: transparent;
  }
  .ant-input:focus {
    box-shadow: none;
  }
}
.ant-message {
  z-index: 99999999 !important;
}
</style>
