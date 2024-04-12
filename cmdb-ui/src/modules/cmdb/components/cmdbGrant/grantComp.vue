<template>
  <div class="cmdb-grant" :style="{ maxHeight: `${windowHeight - 130}px` }">
    <template v-if="cmdbGrantType.includes('ci_type')">
      <div class="cmdb-grant-title">{{ $t('cmdb.components.ciTypeGrant') }}</div>
      <CiTypeGrant
        :CITypeId="CITypeId"
        :tableData="tableData"
        grantType="ci_type"
        @grantDepart="grantDepart"
        @grantRole="grantRole"
        @getTableData="getTableData"
        ref="grant_ci_type"
        :addedRids="addedRids"
      />
    </template>
    <template
      v-if="
        cmdbGrantType.includes('ci_type,ci') || (cmdbGrantType.includes('ci') && !cmdbGrantType.includes('ci_type'))
      "
    >
      <div class="cmdb-grant-title">{{ $t('cmdb.components.ciGrant') }}</div>
      <CiTypeGrant
        :CITypeId="CITypeId"
        :tableData="tableData"
        grantType="ci"
        @grantDepart="grantDepart"
        @grantRole="grantRole"
        @getTableData="getTableData"
        @openReadGrantModal="openReadGrantModal"
        ref="grant_ci"
        :addedRids="addedRids"
      />
    </template>
    <template v-if="cmdbGrantType.includes('type_relation')">
      <div class="cmdb-grant-title">{{ $t('cmdb.components.relationGrant') }}</div>
      <TypeRelationGrant
        :typeRelationIds="typeRelationIds"
        :tableData="tableData"
        grantType="type_relation"
        @grantDepart="grantDepart"
        @grantRole="grantRole"
        @getTableData="getTableData"
        ref="grant_type_relation"
        :addedRids="addedRids"
      />
    </template>
    <template v-if="cmdbGrantType.includes('relation_view')">
      <div class="cmdb-grant-title">{{ resourceTypeName }}{{ $t('cmdb.components.perm') }}</div>
      <RelationViewGrant
        :resourceTypeName="resourceTypeName"
        :tableData="tableData"
        grantType="relation_view"
        @grantDepart="grantDepart"
        @grantRole="grantRole"
        @getTableData="getTableData"
        ref="grant_relation_view"
        :addedRids="addedRids"
      />
    </template>

    <GrantModal ref="grantModal" @handleOk="handleOk" />
    <ReadGrantModal ref="readGrantModal" :CITypeId="CITypeId" @updateTableDataRead="updateTableDataRead" />
  </div>
</template>

<script>
import { mapState } from 'vuex'
import CiTypeGrant from './ciTypeGrant.vue'
import TypeRelationGrant from './typeRelationGrant.vue'
import { searchResource } from '@/modules/acl/api/resource'
import { getResourcePerms } from '@/modules/acl/api/permission'
import GrantModal from './grantModal.vue'
import ReadGrantModal from './readGrantModal'
import RelationViewGrant from './relationViewGrant.vue'
import { getCITypeGroupById, ciTypeFilterPermissions } from '../../api/CIType'

export default {
  name: 'GrantComp',
  components: { CiTypeGrant, TypeRelationGrant, RelationViewGrant, GrantModal, ReadGrantModal },
  props: {
    CITypeId: {
      type: Number,
      default: null,
    },
    resourceTypeName: {
      type: String,
      default: '',
    },
    resourceType: {
      type: String,
      default: 'CIType',
    },
    app_id: {
      type: String,
      default: 'cmdb',
    },
    cmdbGrantType: {
      type: String,
      default: 'ci_type,ci',
    },
    typeRelationIds: {
      type: Array,
      default: null,
    },
    isModal: {
      type: Boolean,
      default: false,
    },
  },
  inject: ['resource_type'],
  data() {
    return {
      tableData: [],
      grantType: '',
      resource_id: null,
      attrGroup: [],
      filerPerimissions: {},
      loading: false,
      addedRids: [], // added rid this time
    }
  },
  computed: {
    ...mapState({
      allEmployees: (state) => state.user.allEmployees,
      allDepartments: (state) => state.user.allDepartments,
    }),
    child_resource_type() {
      return this.resource_type()
    },
    windowHeight() {
      return this.$store.state.windowHeight
    },
  },
  provide() {
    return {
      attrGroup: () => {
        return this.attrGroup
      },
      filerPerimissions: () => {
        return this.filerPerimissions
      },
      loading: () => {
        return this.loading
      },
      isModal: this.isModal,
    }
  },
  watch: {
    resourceTypeName: {
      immediate: true,
      handler() {
        this.init()
      },
    },
    CITypeId: {
      immediate: true,
      handler() {
        if (this.CITypeId && this.cmdbGrantType.includes('ci')) {
          this.getFilterPermissions()
          this.getAttrGroup()
        }
      },
    },
  },
  mounted() {},
  methods: {
    getAttrGroup() {
      getCITypeGroupById(this.CITypeId, { need_other: true }).then((res) => {
        this.attrGroup = res
      })
    },
    getFilterPermissions() {
      ciTypeFilterPermissions(this.CITypeId).then((res) => {
        this.filerPerimissions = res
      })
    },
    async init() {
      const _find = this.child_resource_type.groups.find((item) => item.name === this.resourceType)
      const resource_type_id = _find?.id ?? 0
      const res = await searchResource({
        app_id: this.app_id,
        resource_type_id,
        page_size: 9999,
      })
      const _tempFind = res.resources.find((item) => item.name === this.resourceTypeName)
      console.log(this.resourceTypeName)
      this.resource_id = _tempFind?.id || 0
      this.getTableData()
    },
    async getTableData() {
      this.loading = true
      const _tableData = await getResourcePerms(this.resource_id, { need_users: 0 })
      const perms = []
      for (const key in _tableData) {
        const obj = {}
        obj.name = key
        _tableData[key].perms.forEach((perm) => {
          obj[`${perm.name}`] = true
          obj.rid = perm?.rid ?? null
        })
        perms.push(obj)
      }
      this.tableData = perms
      this.loading = false
    },
    // Grant the department in common-setting and get the roleid from it
    grantDepart(grantType) {
      this.$refs.grantModal.open('depart')
      this.grantType = grantType
    },
    // Grant the oldest role permissions
    grantRole(grantType) {
      this.$refs.grantModal.open('role')
      this.grantType = grantType
    },
    handleOk(params, type) {
      const { grantType } = this
      let rids
      if (type === 'depart') {
        rids = [
          ...params.department.map((rid) => {
            const _find = this.allDepartments.find((dep) => dep.acl_rid === rid)
            return { rid, name: _find?.department_name ?? rid }
          }),
          ...params.user.map((rid) => {
            const _find = this.allEmployees.find((dep) => dep.acl_rid === rid)
            return { rid, name: _find?.nickname ?? rid }
          }),
        ]
      }
      if (type === 'role') {
        rids = [
          ...params.map((role) => {
            return { rid: role.id, name: role.name }
          }),
        ]
      }
      if (grantType === 'ci_type') {
        this.tableData.unshift(
          ...rids.map(({ rid, name }) => {
            const _find = this.tableData.find((item) => item.rid === rid)
            return {
              rid,
              name,
              conifg: false,
              grant: false,
              ..._find,
            }
          })
        )
      }
      if (grantType === 'ci') {
        this.tableData.unshift(
          ...rids.map(({ rid, name }) => {
            const _find = this.tableData.find((item) => item.rid === rid)
            return {
              rid,
              name,
              read_attr: false,
              read_ci: false,
              create: false,
              update: false,
              delete: false,
              ..._find,
            }
          })
        )
      }
      if (grantType === 'type_relation') {
        this.tableData.unshift(
          ...rids.map(({ rid, name }) => {
            return {
              rid,
              name,
              create: false,
              grant: false,
              delete: false,
            }
          })
        )
      }
      if (grantType === 'relation_view') {
        this.tableData.unshift(
          ...rids.map(({ rid, name }) => {
            return {
              rid,
              name,
              read: false,
              grant: false,
            }
          })
        )
      }
      this.addedRids = rids
      this.$nextTick(() => {
        setTimeout(() => {
          this.$refs[`grant_${grantType}`].$refs.xTable.elemStore['main-body-wrapper'].scrollTo(0, 0)
        }, 300)
      })
    },
    openReadGrantModal(col, row) {
      this.$refs.readGrantModal.open(col, row)
    },
    updateTableDataRead(row, hasRead) {
      const _idx = this.tableData.findIndex((item) => item.rid === row.rid)
      this.$set(this.tableData, _idx, { ...this.tableData[_idx], read: hasRead })
      this.getFilterPermissions()
    },
  },
}
</script>

<style lang="less" scoped>
.cmdb-grant {
  position: relative;
  padding: 0 20px;
  overflow: auto;
  .cmdb-grant-title {
    border-left: 4px solid @primary-color;
    padding-left: 10px;
  }
}
</style>

<style lang="less">

.cmdb-grant {
  .grant-button {
    padding: 6px 8px;
    color: @primary-color;
    background-color: @primary-color_5;
    border-radius: 2px;
    cursor: pointer;
    margin: 15px 0;
    display: inline-block;
    transition: all 0.3s;
    &:hover {
      box-shadow: 2px 3px 4px @primary-color_5;
    }
  }
}
</style>
