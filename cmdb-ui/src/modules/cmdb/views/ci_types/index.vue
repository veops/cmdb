<template>
  <div class="ci-types-wrap" :style="{ height: `${windowHeight - 66}px` }">
    <div v-if="!CITypeGroups.length" class="ci-types-empty">
      <a-empty :image="emptyImage" description=""></a-empty>
      <a-button icon="plus" size="small" type="primary" @click="handleClickAddGroup">{{
        $t('cmdb.ciType.addGroup')
      }}</a-button>
    </div>
    <SplitPane
      v-else
      :min="280"
      :max="500"
      :paneLengthPixel.sync="paneLengthPixel"
      appName="cmdb-ci-types"
      triggerColor="#F0F5FF"
      :triggerLength="18"
    >
      <template #one>
        <div class="ci-types-left">
          <div class="ci-types-left-title">
            <a-button
              :disabled="!permissions.includes('admin') && !permissions.includes('cmdb_admin')"
              type="primary"
              size="small"
              icon="plus"
              @click="handleClickAddGroup"
              class="ops-button-primary"
            >{{ $t('cmdb.ciType.group') }}</a-button
            >
            <a-space>
              <a
                @click="
                  () => {
                    $refs.attributeStore.open()
                  }
                "
              >{{ $t('cmdb.ciType.attributeLibray') }}</a
              >
              <a-dropdown v-if="permissions.includes('admin') || permissions.includes('cmdb_admin')">
                <a><ops-icon type="ops-menu"/></a>
                <a-menu slot="overlay">
                  <a-menu-item key="0">
                    <a-upload
                      name="file"
                      accept=".json"
                      :showUploadList="false"
                      style="display: inline-block"
                      action="/api/v0.1/ci_types/template/import/file"
                      @change="changeUploadFile"
                    >
                      <a><a-icon type="upload"/></a><a> {{ $t('upload') }}</a>
                    </a-upload>
                  </a-menu-item>
                  <a-menu-item key="1">
                    <a-space>
                      <a
                        href="/api/v0.1/ci_types/template/export/file"
                      ><a-icon type="download" /> {{ $t('download') }}</a
                      >
                    </a-space>
                  </a-menu-item>
                </a-menu>
              </a-dropdown>
            </a-space>
          </div>
          <draggable class="ci-types-left-content" :list="CITypeGroups" @end="handleChangeGroups" filter=".undraggable">
            <div v-for="g in CITypeGroups" :key="g.id || g.name">
              <div
                :class="
                  `${currentGId === g.id && !currentCId ? 'selected' : ''} ci-types-left-group ${
                    g.id === -1 ? 'undraggable' : ''
                  }`
                "
                @click="handleClickGroup(g.id)"
              >
                <div>
                  <OpsMoveIcon
                    style="width: 17px; height: 17px; display: none; position: absolute; left: -3px; top: 10px"
                  />
                  <span style="font-weight: 700">{{ g.name || $t('other') }}</span>
                  <span :style="{ color: '#c3cdd7' }">({{ g.ci_types.length }})</span>
                </div>
                <a-space>
                  <a-tooltip>
                    <template slot="title">{{ $t('cmdb.ciType.addCITypeInGroup') }}</template>
                    <a><a-icon type="plus" @click="handleCreate(g)"/></a>
                  </a-tooltip>
                  <template v-if="g.id !== -1">
                    <a-tooltip>
                      <template slot="title">{{ $t('cmdb.ciType.editGroup') }}</template>
                      <a><a-icon type="edit" @click="handleEditGroup(g)"/></a>
                    </a-tooltip>
                    <a-tooltip>
                      <template slot="title">{{ $t('cmdb.ciType.deleteGroup') }}</template>
                      <a style="color: red"><a-icon type="delete" @click="handleDeleteGroup(g)"/></a>
                    </a-tooltip>
                  </template>
                </a-space>
              </div>
              <draggable
                v-model="g.ci_types"
                group="ciType"
                :animation="100"
                @start="start(g)"
                @end="end(g)"
                @add="add(g)"
              >
                <div
                  v-for="ci in g.ci_types"
                  :key="ci.id"
                  :class="`${currentCId === ci.id ? 'selected' : ''} ci-types-left-detail`"
                  @click="handleClickCIType(g.id, ci.id, ci.name)"
                >
                  <div>
                    <OpsMoveIcon
                      style="width: 17px; height: 17px; display: none; position: absolute; left: 15px; top: 5px"
                    />
                    <span class="ci-types-left-detail-icon">
                      <template v-if="ci.icon">
                        <img
                          v-if="ci.icon.split('$$')[2]"
                          :src="`/api/common-setting/v1/file/${ci.icon.split('$$')[3]}`"
                        />
                        <ops-icon
                          v-else
                          :style="{
                            color: ci.icon.split('$$')[1],
                            fontSize: '14px',
                          }"
                          :type="ci.icon.split('$$')[0]"
                        />
                      </template>
                      <span :style="{ color: '#2f54eb' }" v-else>{{ ci.name[0].toUpperCase() }}</span>
                    </span>
                  </div>
                  <span class="ci-types-left-detail-title">{{ ci.alias || ci.name }}</span>
                  <a-space class="ci-types-left-detail-action">
                    <a><a-icon type="user-add" @click="(e) => handlePerm(e, ci)"/></a>
                    <a><a-icon type="edit" @click="(e) => handleEdit(e, ci)"/></a>
                    <a
                      v-if="permissions.includes('admin') || permissions.includes('cmdb_admin')"
                      :disabled="ci.inherited"
                      @click="(e) => handleDownloadCiType(e, ci)"
                    >
                      <a-icon type="download" />
                    </a>
                    <a style="color: red" @click="(e) => handleDelete(e, ci)"><a-icon type="delete"/></a>
                  </a-space>
                </div>
              </draggable>
            </div>
          </draggable>
        </div>
      </template>
      <template #two>
        <div class="ci-types-right">
          <CITypeDetail v-if="currentCId" :CITypeId="currentCId" :CITypeName="currentCName" />
          <div v-else class="ci-types-right-empty">
            <a-empty :image="emptyImage" description=""></a-empty>
            <a-button icon="plus" size="small" type="primary" @click="handleCreateCiFromEmpty">{{
              $t('cmdb.ciType.addCIType')
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
        <a-form-item :label="$t('cmdb.ciType.CITypeName')">
          <a-input
            name="name"
            :placeholder="$t('cmdb.ciType.English')"
            v-decorator="[
              'name',
              {
                rules: [
                  { required: true, message: $t('cmdb.ciType.inputAttributeName') },
                  {
                    message: $t('cmdb.ciType.attributeNameTips'),
                    pattern: RegExp('^(?!\\d)[a-zA-Z_0-9]+$'),
                  },
                ],
              },
            ]"
          />
        </a-form-item>
        <a-form-item :label="$t('alias')">
          <a-input name="alias" v-decorator="['alias', { rules: [] }]" />
        </a-form-item>
        <a-form-item :label="$t('cmdb.ciType.isInherit')">
          <a-radio-group v-model="isInherit">
            <a-radio :value="true">
              是
            </a-radio>
            <a-radio :value="false">
              否
            </a-radio>
          </a-radio-group>
        </a-form-item>
        <a-form-item v-if="isInherit" :label="$t('cmdb.ciType.inheritType')">
          <CMDBTypeSelect
            multiple
            :placeholder="$t('cmdb.ciType.inheritTypePlaceholder')"
            v-decorator="[
              'parent_ids',
              { rules: [{ required: true, message: $t('cmdb.ciType.inheritTypePlaceholder') }] },
            ]"
            selectType="ci_type"
            :class="{
              'custom-treeselect': true,
            }"
            :style="{
              '--custom-height': '32px',
              lineHeight: '32px',
              '--custom-multiple-lineHeight': '14px',
            }"
          />
        </a-form-item>
        <a-form-item :label="$t('icon')">
          <IconArea class="ci_types-icon-area" ref="iconArea" />
        </a-form-item>
        <a-form-item :label="$t('cmdb.ciType.defaultSort')" v-if="drawerTitle === $t('cmdb.ciType.editCIType')">
          <el-select
            size="small"
            filterable
            clearable
            v-decorator="[
              'default_order_attr',
              { rules: [{ required: false, message: $t('cmdb.ciType.selectDefaultOrderAttr') }] },
            ]"
          >
            <el-option
              :key="item.name"
              :value="item.name"
              v-for="item in orderSelectionOptions"
              :label="item.alias || item.name"
            >
              <span> {{ item.alias || item.name }}</span>
              <span :title="item.name" style="font-size: 10px; color: #afafaf"> {{ item.name }}</span>
            </el-option>
            <a-divider :style="{ margin: '5px 0' }" />
            <div :style="{ textAlign: 'right' }">
              <a-radio-group v-model="default_order_asc">
                <a-radio value="1">
                  {{ $t('cmdb.ciType.asec') }}
                </a-radio>
                <a-radio value="2">
                  {{ $t('cmdb.ciType.desc') }}
                </a-radio>
              </a-radio-group>
            </div>
          </el-select>
        </a-form-item>
        <a-form-item :label="$t('cmdb.ciType.uniqueKey')">
          <el-select
            size="small"
            filterable
            optionFilterProp="children"
            name="unique_key"
            :filter-method="filterOption"
            v-decorator="['unique_key', { rules: [{ required: true, message: $t('cmdb.ciType.uniqueKeySelect') }] }]"
            :placeholder="$t('placeholder2')"
            @visible-change="
              () => {
                filterInput = ''
              }
            "
          >
            <el-option
              :key="item.id"
              :value="item.id"
              v-for="item in filterAttributes"
              :label="item.alias || item.name"
            >
              <span> {{ item.alias || item.name }}</span>
              <span :title="item.name" style="font-size: 10px; color: #afafaf"> {{ item.name }}</span>
            </el-option>
          </el-select>
          <a-divider type="vertical" />
          <a @click="handleCreatNewAttr">{{ $t('cmdb.ciType.notfound') }}</a>
        </a-form-item>
        <div v-if="newAttrAreaVisible" :style="{ padding: '15px 8px 0 8px', backgroundColor: '#fafafa' }">
          <create-new-attribute
            ref="createNewAttribute"
            @done="handleCreateNewAttrDone"
            @cancel="newAttrAreaVisible = false"
          ></create-new-attribute>
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
    </CustomDrawer>
    <CMDBGrant ref="cmdbGrant" resourceType="CIType" app_id="cmdb" />
    <AttributeStore ref="attributeStore" />
  </div>
</template>

<script>
import _ from 'lodash'
import router, { resetRouter } from '@/router'
import store from '@/store'
import draggable from 'vuedraggable'
import { Select, Option } from 'element-ui'
import {
  createCIType,
  updateCIType,
  deleteCIType,
  getCIType,
  postCiTypeInheritance,
  deleteCiTypeInheritance,
} from '@/modules/cmdb/api/CIType'
import {
  getCITypeGroupsConfig,
  postCITypeGroup,
  putCITypeGroupByGId,
  deleteCITypeGroup,
  putCITypeGroups,
} from '@/modules/cmdb/api/ciTypeGroup'
import { searchAttributes, getCITypeAttributesById } from '@/modules/cmdb/api/CITypeAttr'
import CreateNewAttribute from './ceateNewAttribute.vue'
import CITypeDetail from './ciTypedetail.vue'
import emptyImage from '@/assets/data_empty.png'
import { searchResourceType } from '@/modules/acl/api/resource'
import { roleHasPermissionToGrant } from '@/modules/acl/api/permission'
import IconArea from './iconArea.vue'
import SplitPane from '@/components/SplitPane'
import CMDBGrant from '../../components/cmdbGrant'
import { ops_move_icon as OpsMoveIcon } from '@/core/icons'
import AttributeStore from './attributeStore.vue'
import { getAllDepAndEmployee } from '@/api/company'
import CMDBTypeSelect from '../../components/CMDBTypeSelect'

export default {
  name: 'CITypes',
  components: {
    draggable,
    CreateNewAttribute,
    CITypeDetail,
    CMDBGrant,
    ElSelect: Select,
    ElOption: Option,
    IconArea,
    SplitPane,
    OpsMoveIcon,
    AttributeStore,
    CMDBTypeSelect,
  },
  inject: ['reload'],
  data() {
    return {
      emptyImage,
      modalTitle: this.$t('cmdb.ciType.addGroup'),
      modalVisible: false,
      editingGroup: null,
      editingInput: '',

      CITypeGroups: [],
      allAttributes: [],
      currentId: null,

      form: this.$form.createForm(this),
      drawerVisible: false,
      drawerTitle: '',
      selectGroup: {}, // add CIType in group

      formLayout: 'horizontal',
      newAttrAreaVisible: false,

      resource_type: {},

      paneLengthPixel: 280,
      loading: false,

      startId: null,
      startGroup: null,
      endId: null,
      addId: null,

      filterInput: '',

      orderSelectionOptions: [],
      default_order_asc: '1',

      allTreeDepAndEmp: [],

      editCiType: null,
      isInherit: false,
    }
  },
  computed: {
    formItemLayout() {
      const { formLayout } = this
      return formLayout === 'horizontal'
        ? {
            labelCol: { span: 4 },
            wrapperCol: { span: 16 },
          }
        : {}
    },
    windowHeight() {
      return this.$store.state.windowHeight
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
    currentCName() {
      if (this.currentId) {
        console.log(this.currentId)
        if (this.currentId.split('%')[2] !== 'null') {
          return this.currentId.split('%')[2]
        }
        return null
      }
      return null
    },
    filterAttributes() {
      // unique key, excludes: choice  password computed json
      const _attributes = this.allAttributes.filter(
        (item) => !item.is_choice && !item.is_computed && !['6', '7'].includes(item.value_type)
      )
      if (this.filterInput) {
        return _attributes.filter(
          (item) =>
            item.name.toLowerCase().includes(this.filterInput.toLowerCase()) ||
            item.alias.toLowerCase().includes(this.filterInput.toLowerCase())
        )
      }
      return _attributes
    },
  },
  provide() {
    return {
      resource_type: () => {
        return this.resource_type
      },
      provide_allTreeDepAndEmp: () => {
        return this.allTreeDepAndEmp
      },
    }
  },
  mounted() {
    this.getAllDepAndEmployee()
    const _currentId = localStorage.getItem('ops_cityps_currentId')
    if (_currentId) {
      this.currentId = _currentId
    }
    searchResourceType({ page_size: 9999, app_id: 'cmdb' }).then((res) => {
      this.resource_type = { groups: res.groups, id2perms: res.id2perms }
    })
    this.loadCITypes(!_currentId)
    this.getAttributes()
  },
  methods: {
    getAllDepAndEmployee() {
      getAllDepAndEmployee({ block: 0 }).then((res) => {
        this.allTreeDepAndEmp = res
      })
    },
    async loadCITypes(isResetCurrentId = false) {
      const groups = await getCITypeGroupsConfig({ need_other: true })
      let alreadyReset = false
      if (isResetCurrentId) {
        this.currentId = null
      }
      this.$nextTick(() => {
        groups.forEach((g) => {
          if (!g.id) {
            // Add a fake id to ungrouped
            g.id = -1
          }
          if (isResetCurrentId && !alreadyReset && g.ci_types && g.ci_types.length) {
            this.currentId = `${g.id}%${g.ci_types[0].id}%${g.ci_types[0].name}`
            alreadyReset = true
          }
          if (!g.ci_types) {
            g.ci_types = []
          }
        })
        this.CITypeGroups = groups
        localStorage.setItem('ops_cityps_currentId', this.currentId)
      })
    },
    getAttributes() {
      searchAttributes({ page_size: 10000 }).then((res) => {
        this.allAttributes = res.attributes
      })
    },
    handleClickAddGroup() {
      this.editingGroup = {}
      this.editingInput = ''
      this.modalTitle = this.$t('cmdb.ciType.addGroup')
      this.modalVisible = true
    },
    async handleSubmitEditGroup() {
      if (this.editingGroup && this.editingGroup.id && this.editingGroup.id !== -1) {
        await putCITypeGroupByGId(this.editingGroup.id, {
          name: this.editingInput,
          type_ids: this.editingGroup.ci_types.map((i) => i.id),
        })
        this.$message.success(this.$t('updateSuccess'))
      } else {
        const { id } = await postCITypeGroup({ name: this.editingInput })
        this.currentId = `${id}%null%null`
        this.$message.success(this.$t('addSuccess'))
      }
      this.modalVisible = false
      localStorage.setItem('ops_cityps_currentId', this.currentId)
      this.loadCITypes()
    },
    handleClickGroup(gId) {
      this.currentId = null
      this.$nextTick(() => {
        this.currentId = `${gId}%null%null`
        localStorage.setItem('ops_cityps_currentId', this.currentId)
      })
    },
    handleClickCIType(gId, cId, cName) {
      this.currentId = null
      this.$nextTick(() => {
        this.currentId = `${gId}%${cId}%${cName}`
        localStorage.setItem('ops_cityps_currentId', this.currentId)
      })
    },
    handleCreate(g) {
      this.drawerTitle = this.$t('cmdb.ciType.addCIType')
      this.drawerVisible = true
      this.selectGroup = g
      this.$nextTick(() => {
        this.$refs.iconArea.setIcon()
      })
    },
    handleCreateCiFromEmpty() {
      this.drawerTitle = this.$t('cmdb.ciType.addCIType')
      this.drawerVisible = true
      const _find = this.CITypeGroups.find((item) => item.id === this.currentGId)
      this.selectGroup = _find
      this.$nextTick(() => {
        this.$refs.iconArea.setIcon()
      })
    },
    handleEditGroup(g) {
      this.editingGroup = g
      this.editingInput = g.name
      this.modalTitle = this.$t('cmdb.ciType.editGroup')
      this.modalVisible = true
    },
    async handleDeleteGroup(g) {
      if (g.ci_types && g.ci_types.length > 0) {
        this.$message.error(this.$t('cmdb.ciType.cannotDeleteGroupTips'))
        return
      }
      const that = this
      this.$confirm({
        title: that.$t('warning'),
        content: that.$t('cmdb.ciType.confirmDeleteGroup', { groupName: `${g.name}` }),
        onOk() {
          deleteCITypeGroup(g.id).then((res) => {
            that.$message.info(that.$t('deleteSuccess'))
            that.loadCITypes(true)
          })
        },
      })
    },
    onClose() {
      this.filterInput = ''
      this.form.resetFields()
      this.drawerVisible = false
      this.isInherit = false
    },
    handleCreateNewAttrDone() {
      this.getAttributes()
      this.newAttrAreaVisible = false
    },
    filterOption(input) {
      this.filterInput = input
    },
    async handleSubmit(e) {
      e.preventDefault()
      this.form.validateFields(async (err, values) => {
        if (!err) {
          this.loading = true
          if (values.default_order_attr && this.default_order_asc === '2') {
            values.default_order_attr = `-${values.default_order_attr}`
          }
          const _icon = this.$refs.iconArea.getIcon()
          const icon =
            _icon && _icon.name ? `${_icon.name}$$${_icon.color || ''}$$${_icon.id || ''}$$${_icon.url || ''}` : ''
          if (values.id) {
            const { parent_ids: oldP = [] } = this.editCiType
            const { parent_ids: newP = [] } = values
            const { remove, add } = this.compareArrays(newP, oldP)
            if (add && add.length) {
              await postCiTypeInheritance({ parent_ids: add, child_id: values.id }).catch(() => {
                this.loading = false
              })
            }
            if (remove && remove.length) {
              for (let i = 0; i < remove.length; i++) {
                await deleteCiTypeInheritance({ parent_id: remove[i], child_id: values.id }).catch(() => {
                  this.loading = false
                })
              }
            }
            delete values.parent_ids
            await this.updateCIType(values.id, {
              ...values,
              icon,
            })
          } else {
            await this.createCIType({ ...values, icon })
          }
        }
      })
    },
    compareArrays(newArr, oldArr) {
      const remove = []
      const add = []
      for (let i = 0; i < oldArr.length; i++) {
        const item = oldArr[i]
        if (newArr.indexOf(item) === -1) {
          remove.push(item)
        }
      }
      for (let i = 0; i < newArr.length; i++) {
        const item = newArr[i]
        if (oldArr.indexOf(item) === -1) {
          add.push(item)
        }
      }
      return { remove, add }
    },
    start(g) {
      console.log('start', g)
      this.startId = g.id
      this.startGroup = _.cloneDeep(g)
    },
    end(g) {
      console.log('end', g)
      this.endId = g.id
      const that = this
      if (this.startId === g.id && g.id !== -1 && this.addId !== -1) {
        // Changing positions within a group
        putCITypeGroupByGId(g.id, { name: g.name, type_ids: g.ci_types.map((i) => i.id) })
          .then(() => {
            this.$message.success(that.$t('saveSuccess'))
          })
          .catch(() => {
            this.loadCITypes(!this.currentId)
          })
          .finally(() => {
            this.startId = null
            this.endId = null
            this.addId = null
          })
      }
      if (this.startId === g.id && g.id !== -1 && this.addId === -1) {
        // Change from one group to another
        const changedCiTypes = this.startGroup.ci_types
          .filter((ciType) => {
            const _find = g.ci_types.find((gCiType) => ciType.id === gCiType.id)
            if (_find) {
              return false
            }
            return true
          })
          .map((item) => item.id)
        deleteCITypeGroup(g.id, { name: g.name, type_ids: changedCiTypes })
          .then(() => {
            this.$message.success(that.$t('saveSuccess'))
          })
          .catch(() => {
            this.loadCITypes(!this.currentId)
          })
          .finally(() => {
            this.startId = null
            this.endId = null
            this.addId = null
          })
      }
    },
    add(g) {
      console.log('add', g)
      this.addId = g.id
      const that = this
      if (g.id && g.id !== -1) {
        // Change positions across groups without changing to others
        putCITypeGroupByGId(g.id, { name: g.name, type_ids: g.ci_types.map((i) => i.id) })
          .then(() => {
            this.$message.success(that.$t('saveSuccess'))
          })
          .catch(() => {
            this.loadCITypes(!this.currentId)
          })
          .finally(() => {
            this.startId = null
            this.endId = null
            this.addId = null
          })
      }
    },
    async handleChangeCITypes(e, g) {
      const that = this
      if (g.id && g.id !== -1) {
        putCITypeGroupByGId(g.id, { name: g.name, type_ids: g.ci_types.map((i) => i.id) })
          .then(() => {
            this.$message.success(that.$t('saveSuccess'))
          })
          .catch(() => {
            this.loadCITypes(!this.currentId)
          })
      }
    },
    async handleChangeGroups() {
      const that = this
      putCITypeGroups({ group_ids: this.CITypeGroups.filter((c) => c.id).map((c) => c.id) })
        .then(() => {
          this.$message.success(that.$t('saveSuccess'))
        })
        .catch(() => {
          this.loadCITypes(!this.currentId)
        })
    },
    async createCIType(data) {
      const { type_id } = await createCIType(data).catch(() => {
        this.loading = false
      })
      this.$message.success(this.$t('addSuccess'))
      if (this.selectGroup && this.selectGroup.id && this.selectGroup.id !== -1) {
        const ids = this.selectGroup.ci_types.map((i) => i.id)
        ids.push(type_id)
        await putCITypeGroupByGId(this.selectGroup.id, {
          name: this.selectGroup.name,
          type_ids: ids,
        })
      }
      this.currentId = `${this.selectGroup?.id || ''}%${type_id}%${data.name}`

      localStorage.setItem('ops_cityps_currentId', this.currentId)
      setTimeout(() => {
        this.loadCITypes()
        this.loading = false
        this.drawerVisible = false
      }, 1000)
    },
    async updateCIType(CITypeId, data) {
      const that = this
      await updateCIType(CITypeId, data)
        .then((res) => {
          this.$message.success(that.$t('updateSuccess'))

          const _currentId = this.currentId
          this.currentId = null
          this.$nextTick(() => {
            this.currentId = _currentId

            localStorage.setItem('ops_cityps_currentId', this.currentId)
            setTimeout(() => {
              this.loadCITypes()
              this.loading = false
              this.drawerVisible = false
            }, 1000)
          })
        })
        .finally(() => {
          this.loading = false
        })
    },
    handleDelete(e, record) {
      e.preventDefault()
      e.stopPropagation()
      const that = this
      this.$confirm({
        title: that.$t('warning'),
        content: that.$t('cmdb.ciType.confirmDeleteCIType', { typeName: `${record.alias || record.name}` }),
        onOk() {
          deleteCIType(record.id).then((res) => {
            that.$message.success(that.$t('deleteSuccess'))
            that.loadCITypes(true)
            that.resetRoute()
          })
        },
      })
    },
    handleDownloadCiType(e, ci) {
      e.preventDefault()
      e.stopPropagation()
      const x = new XMLHttpRequest()
      x.open('GET', `/api/v0.1/ci_types/${ci.id}/template/export`, true)
      x.responseType = 'blob'
      x.onload = function(e) {
        const url = window.URL.createObjectURL(x.response)
        const a = document.createElement('a')
        a.href = url
        a.download = `${ci.alias || ci.name}.json`
        a.click()
      }
      x.send()
    },
    resetRoute() {
      resetRouter()
      const roles = store.getters.roles
      store.dispatch('GenerateRoutes', { roles }, { root: true }).then(() => {
        router.addRoutes(store.getters.appRoutes)
      })
    },
    async handleEdit(e, record) {
      e.preventDefault()
      e.stopPropagation()
      this.drawerTitle = this.$t('cmdb.ciType.editCIType')
      this.drawerVisible = true
      await getCITypeAttributesById(record.id).then((res) => {
        this.orderSelectionOptions = res.attributes.filter((item) => item.is_required)
      })
      await getCIType(record.id).then((res) => {
        const ci_type = res.ci_types[0]
        this.editCiType = ci_type ?? null
        if (ci_type.parent_ids && ci_type.parent_ids.length) {
          this.isInherit = true
          this.$nextTick(() => {
            this.form.setFieldsValue({
              parent_ids: ci_type.parent_ids,
            })
          })
        }
      })
      this.$nextTick(() => {
        this.default_order_asc = record.default_order_attr && record.default_order_attr.startsWith('-') ? '2' : '1'

        this.form.setFieldsValue({
          id: record.id,
          alias: record.alias,
          name: record.name,
          unique_key: record.unique_id,
          default_order_attr:
            record.default_order_attr && record.default_order_attr.startsWith('-')
              ? record.default_order_attr.slice(1)
              : record.default_order_attr,
        })

        this.$refs.iconArea.setIcon(
          record.icon
            ? {
                name: record.icon.split('$$')[0] || '',
                color: record.icon.split('$$')[1] || '',
                id: record.icon.split('$$')[2] ? Number(record.icon.split('$$')[2]) : null,
                url: record.icon.split('$$')[3] || '',
              }
            : {}
        )
      })
    },
    handleCreatNewAttr() {
      this.newAttrAreaVisible = !this.newAttrAreaVisible
      if (this.newAttrAreaVisible) {
        this.$nextTick(() => {
          this.$refs.createNewAttribute.checkCanDefineComputed()
        })
      }
    },
    handlePerm(e, ci) {
      e.preventDefault()
      e.stopPropagation()
      roleHasPermissionToGrant({
        app_id: 'cmdb',
        resource_type_name: 'CIType',
        perm: 'grant',
        resource_name: ci.name,
      }).then((res) => {
        if (res.result) {
          this.$refs.cmdbGrant.open({ name: ci.name, cmdbGrantType: 'ci_type', CITypeId: ci.id })
        } else {
          this.$message.error(this.$t('noPermission'))
        }
      })
    },
    changeUploadFile({ file, fileList, event }) {
      const key = 'upload'
      if (file.status === 'uploading') {
        this.$message.loading({ content: this.$t('cmdb.ciType.uploading'), key, duration: 0 })
      }
      if (file.status === 'done') {
        this.$message.success({ content: this.$t('uploadSuccess'), key, duration: 2 })
        this.reload()
      }
      if (file.status === 'error') {
        this.$message.error({ content: this.$t('cmdb.ciType.uploadFailed'), key, duration: 2 })
      }
    },
  },
}
</script>

<style lang="less" scoped>
.ci-types-wrap {
  margin: 0 0 -24px 0;
  .ci-types-empty {
    position: absolute;
    text-align: center;
    left: 50%;
    top: 40%;
    transform: translate(-50%, -50%);
  }
  .ci-types-left {
    width: 100%;
    overflow: auto;
    float: left;
    border-top-left-radius: 20px;
    border-top-right-radius: 20px;
    .ci-types-left-content {
      max-height: calc(100% - 45px);
      overflow: auto;
    }
    .ci-types-left-title {
      padding: 10px 15px;
      display: flex;
      flex-direction: row;
      justify-content: space-between;
    }
    .ci-types-left-group {
      position: relative;
      padding: 8px 15px;
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
        background-color: #e1efff;
        > div:nth-child(2) {
          display: inline-flex;
        }
        svg {
          display: inline !important;
        }
      }
    }
    .ci-types-left-detail {
      padding: 3px 14px 3px 36px;
      cursor: pointer;
      position: relative;
      display: flex;
      flex-direction: row;
      justify-content: flex-start;
      margin-bottom: 4px;
      .ci-types-left-detail-action {
        display: none;
        margin-left: auto;
      }
      .ci-types-left-detail-icon {
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
        background-color: #e1efff;
        svg {
          display: inline !important;
        }
        .ci-types-left-detail-action {
          display: inline-flex;
        }
      }
    }
    .selected {
      background-color: #e1efff;
      .ci-types-left-detail-title {
        font-weight: 700;
      }
    }
  }
  .ci-types-right {
    width: 100%;
    position: relative;
    .ci-types-right-empty {
      position: absolute;
      text-align: center;
      left: 50%;
      top: 40%;
      transform: translate(-50%, -50%);
    }
  }
  .ci-types-left,
  .ci-types-right {
    height: 100%;
    background-color: #fff;
  }
}
</style>

<style lang="less">
.ci_types-icon-area {
  margin-top: 5px;
  > .icon-area-item > span {
    margin-right: 0 !important;
  }
}
</style>
