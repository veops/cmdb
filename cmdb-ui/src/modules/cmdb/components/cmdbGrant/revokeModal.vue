<template>
  <a-modal :visible="visible" @cancel="handleCancel" @ok="handleOK" :title="$t('revoke')">
    <a-form-model :model="form" :label-col="{ span: 4 }" :wrapper-col="{ span: 16 }">
      <a-form-model-item :label="$t('user')">
        <EmployeeTreeSelect
          class="custom-treeselect custom-treeselect-bgcAndBorder"
          :style="{
            '--custom-height': '32px',
            lineHeight: '32px',
            '--custom-bg-color': '#fff',
            '--custom-border': '1px solid #d9d9d9',
            '--custom-multiple-lineHeight': '18px',
          }"
          :multiple="true"
          v-model="form.users"
          :placeholder="$t('cmdb.serviceTree.userPlaceholder')"
          :idType="2"
          departmentKey="acl_rid"
          employeeKey="acl_rid"
        />
      </a-form-model-item>
      <a-form-model-item :label="$t('role')">
        <treeselect
          v-model="form.roles"
          :multiple="true"
          :options="filterAllRoles"
          class="custom-treeselect custom-treeselect-bgcAndBorder"
          :style="{
            '--custom-height': '32px',
            lineHeight: '32px',
            '--custom-bg-color': '#fff',
            '--custom-border': '1px solid #d9d9d9',
            '--custom-multiple-lineHeight': '18px',
          }"
          :limit="10"
          :limitText="(count) => `+ ${count}`"
          :normalizer="
            (node) => {
              return {
                id: node.id,
                label: node.name,
              }
            }
          "
          appendToBody
          zIndex="1050"
          :placeholder="$t('cmdb.serviceTree.rolePlaceholder')"
          @search-change="searchRole"
        />
      </a-form-model-item>
    </a-form-model>
  </a-modal>
</template>

<script>
import EmployeeTreeSelect from '@/views/setting/components/employeeTreeSelect.vue'
import { getAllDepAndEmployee } from '@/api/company'
import { searchRole } from '@/modules/acl/api/role'

export default {
  name: 'RevokeModal',
  components: { EmployeeTreeSelect },
  data() {
    return {
      visible: false,
      form: {
        users: undefined,
        roles: undefined,
      },
      allTreeDepAndEmp: [],
      allRoles: [],
      filterAllRoles: [],
    }
  },
  provide() {
    return {
      provide_allTreeDepAndEmp: () => {
        return this.allTreeDepAndEmp
      },
    }
  },
  mounted() {
    this.getAllDepAndEmployee()
    this.loadRoles()
  },
  methods: {
    async loadRoles() {
      const res = await searchRole({ page_size: 9999, app_id: 'cmdb', is_all: true })
      this.allRoles = res.roles
      this.filterAllRoles = this.allRoles.slice(0, 100)
    },
    getAllDepAndEmployee() {
      getAllDepAndEmployee({ block: 0 }).then((res) => {
        this.allTreeDepAndEmp = res
      })
    },
    open() {
      this.visible = true
      this.$nextTick(() => {
        this.form = {
          users: undefined,
          roles: undefined,
        }
      })
    },
    handleCancel() {
      this.visible = false
    },
    searchRole(searchQuery) {
      this.filterAllRoles = this.allRoles
        .filter((item) => item.name.toLowerCase().includes(searchQuery.toLowerCase()))
        .slice(0, 100)
    },
    handleOK() {
      this.$emit('handleRevoke', this.form)
      this.handleCancel()
    },
  },
}
</script>

<style></style>
