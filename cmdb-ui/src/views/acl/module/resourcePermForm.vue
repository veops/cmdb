<template>
  <a-modal
    :title="drawerTitle"
    v-model="drawerVisible"
    width="50%"
  >
    <template slot="footer">
      <a-button key="back" @click="handleCancel">{{ $t('tip.close') }}</a-button>
    </template>

    <template>
      <a-list itemLayout="horizontal">
        <a-list-item v-for="item in resPerms" :key="item[0]">
          <span>{{ item[0] }}：  </span>
          <div>
            <a-tag
              closable
              color="cyan"
              v-for="perm in item[1]"
              :key="perm.name"
              @close="deletePerm(perm.rid, perm.name)">
              {{ perm.name }}
            </a-tag>
          </div>
        </a-list-item>
      </a-list>
    </template>
  </a-modal>

</template>

<script>
import { STable } from '@/components'
import { getResourceTypePerms, getResourcePerms, deleteRoleResourcePerm } from '@/api/acl/permission'

export default {
  name: 'ResourceForm',
  components: {
    STable
  },
  data () {
    return {
      drawerTitle: this.$t('acl.permList'),
      drawerVisible: false,
      record: null,
      allPerms: [],
      resPerms: [],
      roleID: null,
      childrenDrawer: false,
      allRoles: []
    }
  },

  beforeCreate () {
    this.form = this.$form.createForm(this)
  },
  methods: {
    handlePerm (record) {
      this.drawerVisible = true
      this.record = record
      this.getResPerms(record.id)

      this.$nextTick(() => {
        this.getAllPerms(record.resource_type_id)
      })
    },
    getResPerms (resId) {
      getResourcePerms(resId).then(res => {
        var perms = []
        for (var key in res) {
          perms.push([key, res[key]])
        }
        this.resPerms = perms
      })
    },
    getAllPerms (resTypeId) {
      getResourceTypePerms(resTypeId).then(res => {
        this.allPerms = res
      })
    },
    deletePerm (roleID, permName) {
      deleteRoleResourcePerm(roleID, this.record.id, { perms: [permName] }).then(res => {
        this.$message.success(this.$t('tip.deleteSuccess'))
      }).catch(err => this.requestFailed(err))
    },
    handleCancel (e) {
      this.drawerVisible = false
    },
    requestFailed (err) {
      console.log(err)
      const msg = ((err.response || {}).data || {}).message || this.$t('tip.requestFailed')
      this.$message.error(`${msg}`)
    }

  },
  watch: {}

}
</script>

<style lang="less" scoped>
  .search {
    margin-bottom: 54px;
  }

  .fold {
    width: calc(100% - 216px);
    display: inline-block
  }

  .operator {
    margin-bottom: 18px;
  }
  .action-btn {
    margin-bottom: 1rem;
  }

  @media screen and (max-width: 900px) {
    .fold {
      width: 100%;
    }
  }
</style>
