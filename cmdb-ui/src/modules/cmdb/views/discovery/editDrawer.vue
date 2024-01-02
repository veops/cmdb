<template>
  <CustomDrawer width="800px" :title="title" :visible="visible" @close="handleClose">
    <template v-if="adType === 'agent'">
      <a-form-model
        ref="autoDiscoveryForm"
        :model="form"
        :rules="rules"
        :label-col="{ span: 2 }"
        :wrapper-col="{ span: 20 }"
      >
        <a-divider :style="{ margin: '5px 0' }">{{ $t('cmdb.ciType.basicConfig') }}</a-divider>
        <a-form-model-item :label="$t('name')" prop="name">
          <a-input v-model="form.name" />
        </a-form-model-item>
        <a-form-model-item :label="$t('icon')" v-if="is_inner">
          <CustomIconSelect v-model="customIcon" :style="{ marginTop: '6px' }" />
        </a-form-model-item>
        <a-form-model-item :label="$t('cmdb.ad.mode')" prop="is_plugin">
          <a-radio-group v-model="form.is_plugin" @change="changeIsPlugin" :disabled="!is_inner">
            <a-radio :value="false">{{ $t('cmdb.custom_dashboard.default') }}</a-radio>
            <a-radio :value="true">plugin</a-radio>
          </a-radio-group>
        </a-form-model-item>
      </a-form-model>
      <a-divider :style="{ margin: '5px 0' }">{{ $t('cmdb.ad.collectSettings') }}</a-divider>
      <CustomCodeMirror
        codeMirrorId="cmdb-adt"
        v-if="form.is_plugin"
        ref="codemirror"
        @changeCodeContent="changeCodeContent"
      ></CustomCodeMirror>
      <div style="margin:10px 0;text-align:right;">
        <a-button
          v-show="form.is_plugin"
          size="small"
          type="primary"
          ghost
          @click="handleSubmit(true)"
        >{{ $t('cmdb.ad.updateFields') }}</a-button
        >
      </div>
      <a-button
        v-show="!form.is_plugin"
        size="small"
        type="primary"
        ghost
        icon="plus"
        :style="{ marginBottom: '10px' }"
        @click="insertEvent(-1)"
      >{{ $t('new') }}</a-button
      >
      <vxe-table
        size="mini"
        stripe
        class="ops-stripe-table"
        show-overflow
        keep-source
        ref="xTable"
        max-height="400"
        :data="tableData"
        :edit-config="{ trigger: 'manual', mode: 'row' }"
      >
        <vxe-column field="name" :title="$t('name')" :edit-render="{ autofocus: '.vxe-input--inner' }">
          <template #edit="{ row }">
            <vxe-input v-model="row.name" type="text"></vxe-input>
          </template>
        </vxe-column>
        <vxe-column field="type" :title="$t('type')" :edit-render="{}">
          <template #edit="{ row }">
            <vxe-select v-model="row.type" transfer>
              <vxe-option v-for="item in typeList" :key="item" :value="item" :label="item"></vxe-option>
            </vxe-select>
          </template>
        </vxe-column>
        <vxe-column field="desc" :title="$t('desc')" :edit-render="{ autofocus: '.vxe-input--inner' }">
          <template #edit="{ row }">
            <vxe-input v-model="row.desc" type="text"></vxe-input>
          </template>
        </vxe-column>
        <vxe-column :title="$t('operation')" width="60" v-if="!form.is_plugin">
          <template #default="{ row }">
            <a-space v-if="$refs.xTable.isActiveByRow(row)">
              <a @click="saveRowEvent(row)"><a-icon type="save"/></a>
              <a @click="cancelRowEvent(row)"><a-icon type="close"/></a>
            </a-space>
            <a-space v-else>
              <a @click="editRowEvent(row)"><a-icon type="edit"/></a>
              <a :style="{ color: 'red' }" @click="deleteRowEvent(row)"><a-icon type="delete"/></a>
            </a-space>
          </template>
        </vxe-column>
      </vxe-table>

      <div class="custom-drawer-bottom-action">
        <a-button @click="handleClose">{{ $t('cancel') }}</a-button>
        <a-button @click="handleSubmit(false)" type="primary">{{ $t('save') }}</a-button>
      </div>
    </template>
    <template v-else>
      <HttpSnmpAD ref="httpSnmpAd" :ruleType="adType" :ruleName="ruleData.name" />
    </template>
  </CustomDrawer>
</template>

<script>
import CustomIconSelect from '@/components/CustomIconSelect'
import { postDiscovery, putDiscovery } from '../../api/discovery'
import HttpSnmpAD from '../../components/httpSnmpAD'
import CustomCodeMirror from '@/components/CustomCodeMirror'
import 'codemirror/lib/codemirror.css'
import 'codemirror/theme/monokai.css'
export default {
  name: 'EditDrawer',
  components: { CustomIconSelect, CustomCodeMirror, HttpSnmpAD },
  props: {
    is_inner: {
      type: Boolean,
      default: true,
    },
  },
  data() {
    const default_plugin_script = this.$t('cmdb.ad.pluginScript')
    const typeList = ['String', 'Integer', 'Float', 'Date', 'DateTime', 'Time', 'JSON']
    return {
      default_plugin_script,
      typeList,
      visible: false,
      ruleData: {},
      type: 'add',
      adType: '',
      form: { name: '', is_plugin: false },
      rules: {},
      customIcon: { name: '', color: '' },
      tableData: [],
      editDefaultTableData: [],
      plugin_script: '',
      cmOptions: {
        lineNumbers: true,
        mode: 'python',
        height: '200px',
        theme: 'monokai',
        tabSize: 4,
        lineWrapping: true,
      },
    }
  },
  computed: {
    title() {
      if (this.adType === 'http' || this.adType === 'snmp') {
        return this.ruleData.name
      }
      if (this.type === 'edit') {
        return this.$t('edit') + `：${this.ruleData.name}`
      }
      return this.$t('new')
    },
  },
  inject: {
    getDiscovery: {
      from: 'getDiscovery',
      default: () => {},
    },
  },
  methods: {
    open(data, type, adType) {
      this.visible = true
      this.type = type
      this.ruleData = data
      this.adType = adType
      if (!this.is_inner) {
        this.form = {
          name: '',
          is_plugin: true,
        }
      }
      if (adType === 'http' || adType === 'snmp') {
        return
      }
      this.$nextTick(() => {
        if (this.type === 'edit') {
          this.form = {
            name: data.name,
            is_plugin: data.is_plugin,
          }
          this.customIcon = data?.option?.icon ?? { name: 'caise-chajian', color: '' }
          this.tableData = data?.attributes ?? []
          this.editDefaultTableData = data?.attributes ?? []
          this.plugin_script = data?.plugin_script ?? this.default_plugin_script
        }
        if (this.type === 'add') {
          this.customIcon = { name: 'caise-chajian', color: '' }
          // eslint-disable-next-line no-useless-escape
          this.plugin_script = this.default_plugin_script
        }
        if (data?.is_plugin || !this.is_inner) {
          this.$nextTick(() => {
            this.$refs.codemirror.initCodeMirror(this.plugin_script)
          })
        }
      })
    },
    handleClose() {
      this.tableData = []
      this.customIcon = { name: '', color: '' }
      this.form = { name: '', is_plugin: false }
      if (this.adType === 'agent') {
        this.$refs.autoDiscoveryForm.clearValidate()
      } else {
        // this.$refs.httpSnmpAd.currentCate = ''
      }
      this.visible = false
    },
    async insertEvent(row) {
      const $table = this.$refs.xTable
      const record = {}
      const { row: newRow } = await $table.insertAt(record, row)
      await $table.setEditRow(newRow)
    },
    editRowEvent(row) {
      const $table = this.$refs.xTable
      $table.setActiveRow(row)
    },
    saveRowEvent() {
      const $table = this.$refs.xTable
      $table.clearActived().then(() => {
        this.loading = true
        setTimeout(() => {
          this.loading = false
        }, 300)
      })
    },
    cancelRowEvent(row) {
      const $table = this.$refs.xTable
      $table.clearActived().then(() => {
        // Restore row data
        $table.revertData(row)
      })
    },
    deleteRowEvent(row) {
      const $table = this.$refs.xTable
      $table.remove(row)
    },
    async handleSubmit(isUpdateAttr = false) {
      const $table = this.$refs.xTable
      const { fullData: _tableData } = $table.getTableData()
      console.log(_tableData)
      const params = {
        ...this.form,
        type: this.adType,
        is_inner: this.is_inner,
        option: { icon: this.customIcon },
        attributes: this.form.is_plugin
          ? undefined
          : _tableData.map(({ name, alias, desc, type }) => {
              return { name, alias, desc, type }
            }),
        plugin_script: this.form.is_plugin ? this.plugin_script : undefined,
      }
      let res
      if (this.type === 'add') {
        res = await postDiscovery(params)
      } else {
        res = await putDiscovery(this.ruleData.id, params)
      }
      if (isUpdateAttr) {
        this.tableData = res.attributes
        this.type = 'edit'
        this.ruleData = res
        this.$message.success(this.$t('updateSuccess'))
        if (this.is_inner) {
          this.getDiscovery()
        }
        return
      }
      this.handleClose()
      console.log(this.is_inner)
      if (this.is_inner) {
        this.$message.success(this.$t('saveSuccess'))
        this.getDiscovery()
      } else {
        this.$emit('updateNotInner', res)
      }
    },
    changeIsPlugin(e) {
      if (e.target.value) {
        this.$nextTick(() => {
          this.$refs.codemirror.initCodeMirror(this.plugin_script)
        })
      }
    },
    changeCodeContent(value) {
      this.plugin_script = value && value.replace('\t', '    ')
    },
  },
}
</script>

<style></style>
