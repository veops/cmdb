<template>
  <a-modal
    width="600px"
    :bodyStyle="{
      paddingTop: 0,
    }"
    :visible="visible"
    :footer="null"
    @cancel="handleCancel"
    :title="$t('view')"
  >
    <div>
      <template v-if="readCIIdFilterPermissions && readCIIdFilterPermissions.length">
        <p>
          <strong>{{ $t('cmdb.serviceTree.idAuthorizationPolicy') }}</strong>
          <a
            @click="
              () => {
                showAllReadCIIdFilterPermissions = !showAllReadCIIdFilterPermissions
              }
            "
            v-if="readCIIdFilterPermissions.length > 10"
          ><a-icon
            :type="showAllReadCIIdFilterPermissions ? 'caret-down' : 'caret-up'"
          /></a>
        </p>
        <a-tag
          v-for="item in showAllReadCIIdFilterPermissions
            ? readCIIdFilterPermissions
            : readCIIdFilterPermissions.slice(0, 10)"
          :key="item.name"
          color="blue"
          :style="{ marginBottom: '5px' }"
        >{{ item.name }}</a-tag
        >
        <a-tag
          :style="{ marginBottom: '5px' }"
          v-if="readCIIdFilterPermissions.length > 10 && !showAllReadCIIdFilterPermissions"
        >+{{ readCIIdFilterPermissions.length - 10 }}</a-tag
        >
      </template>
      <a-empty v-else>
        <img slot="image" :src="require('@/assets/data_empty.png')" />
        <span slot="description"> {{ $t('noData') }} </span>
      </a-empty>
    </div>
  </a-modal>
</template>

<script>
import { ciTypeFilterPermissions, getCIType } from '../../../api/CIType'
import FilterComp from '@/components/CMDBFilterComp'
import { searchRole } from '@/modules/acl/api/role'

export default {
  name: 'ReadPermissionsModal',
  components: { FilterComp },
  data() {
    return {
      visible: false,
      filerPerimissions: {},
      readCIIdFilterPermissions: [],
      canSearchPreferenceAttrList: [],
      showAllReadCIIdFilterPermissions: false,
      allRoles: [],
    }
  },
  mounted() {
    this.loadRoles()
  },
  methods: {
    async loadRoles() {
      const res = await searchRole({ page_size: 9999, app_id: 'cmdb', is_all: true })
      this.allRoles = res.roles
    },
    async open(treeKey) {
      this.visible = true
      const _splitTreeKey = treeKey.split('@^@').filter((item) => !!item)
      const _treeKey = _splitTreeKey.slice(_splitTreeKey.length - 1, _splitTreeKey.length)[0].split('%')

      const typeId = _treeKey[1]
      const _treeKeyPath = _splitTreeKey.map((item) => item.split('%')[0]).join(',')
      await ciTypeFilterPermissions(typeId).then((res) => {
        this.filerPerimissions = res
      })
      const readCIIdFilterPermissions = []
      Object.entries(this.filerPerimissions).forEach(([k, v]) => {
        const { id_filter } = v
        if (id_filter && Object.keys(id_filter).includes(_treeKeyPath)) {
          const _find = this.allRoles.find((item) => item.id === Number(k))
          readCIIdFilterPermissions.push({ name: _find?.name ?? k, rid: k })
        }
      })
      this.readCIIdFilterPermissions = readCIIdFilterPermissions
      console.log(readCIIdFilterPermissions)
    },
    handleCancel() {
      this.showAllReadCIIdFilterPermissions = false
      this.visible = false
    },
  },
}
</script>

<style></style>
