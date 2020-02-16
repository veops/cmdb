<template>
  <a-card :bordered="false">

    <a-list
      :dataSource="CITypes"
      :grid="{ gutter: 20, column: 4 }"
      class="ci-type-list"
      itemLayout="horizontal"
      size="small"
    >
      <a-list-item slot="renderItem" slot-scope="item">

        <template v-if="Object.keys(item).length === 0">
          <a-button class="new-btn" type="dashed" @click="handleCreate">
            <a-icon type="plus"/>
            {{ $t('ciType.add') }}
          </a-button>
        </template>
        <template v-else>
          <a-card
            :bodyStyle="{padding: '0.9rem 0.8rem'}"
            :hoverable="true"
          >
            <template class="ant-card-actions" slot="actions">
              <router-link
                :to="{ name: 'ci_type_detail', params: { CITypeName: item.name, CITypeId: item.id }}"
              >
                <a-icon type="setting" />
              </router-link>
              <a-icon type="edit" @click="handleEdit(item)"/>
              <a-popconfirm :title="$t('tip.confirmDelete')" @confirm="handleDelete(item)" :okText="$t('button.yes')" :cancelText="$t('button.no')">
                <a-icon type="delete"/>
              </a-popconfirm>
            </template>
            <a-card-meta>
              <div slot="title" style="margin-bottom: 3px">{{ item.alias || item.name }}</div>
              <a-avatar
                :src="item.icon_url"
                class="card-avatar"
                size="large"
                slot="avatar"
                style="color:  #7f9eb2; backgroundColor: #e1eef6; padding-left: -1rem;"
              >
                {{ item.name[0].toUpperCase() }}
              </a-avatar>
              <div class="meta-content" slot="description">{{ item.name }}</div>
            </a-card-meta>

          </a-card>
        </template>

      </a-list-item>

    </a-list>

    <a-drawer
      :closable="false"
      :title="drawerTitle"
      :visible="drawerVisible"
      @close="onClose"
      placement="right"
      width="30%"
    >
      <a-form :form="form" :layout="formLayout" @submit="handleSubmit">

        <a-form-item
          :label-col="formItemLayout.labelCol"
          :wrapper-col="formItemLayout.wrapperCol"
          :label="$t('ciType.name')"
        >
          <a-input
            name="name"
            v-decorator="['name', {rules: [{ required: true, message: $t('ciType.nameRequired')},{message: $t('ciType.nameValidate'), pattern: RegExp('^(?!\\d)[a-zA-Z_0-9]+$')}]} ]"
          />
        </a-form-item>
        <a-form-item
          :label-col="formItemLayout.labelCol"
          :wrapper-col="formItemLayout.wrapperCol"
          :label="$t('ciType.alias')"
        >
          <a-input
            name="alias"
            v-decorator="['alias', {rules: []} ]"
          />
        </a-form-item>

        <a-form-item
          :label-col="formItemLayout.labelCol"
          :wrapper-col="formItemLayout.wrapperCol"
          :label="$t('ciType.unique') + '*'"
        >

          <a-select
            showSearch
            optionFilterProp="children"
            name="unique_key"
            style="width: 200px"
            :filterOption="filterOption"
            v-decorator="['unique_key', {rules: [{required: true}], } ]"

          >
            <a-select-option :key="item.id" :value="item.id" v-for="item in allAttributes">{{ item.alias || item.name }}</a-select-option>
          </a-select>

        </a-form-item>

        <a-form-item>
          <a-input
            name="id"
            type="hidden"
            v-decorator="['id', {rules: []} ]"
          />
        </a-form-item>

        <div
          :style="{
            position: 'absolute',
            left: 0,
            bottom: 0,
            width: '100%',
            borderTop: '1px solid #e9e9e9',
            padding: '0.8rem 1rem',
            background: '#fff',

          }"
        >
          <a-button @click="handleSubmit" type="primary" style="margin-right: 1rem">{{ $t('button.submit') }}</a-button>
          <a-button @click="onClose">{{ $t('button.cancel') }}</a-button>

        </div>
      </a-form>
    </a-drawer>

  </a-card>
</template>

<script>

import { getCITypes, createCIType, updateCIType, deleteCIType } from '@/api/cmdb/CIType'
import { searchAttributes } from '@/api/cmdb/CITypeAttr'

export default {
  name: 'CITypeList',
  components: {},
  data () {
    return {
      CITypes: [],
      allAttributes: [],
      form: this.$form.createForm(this),

      drawerVisible: false,

      drawerTitle: '',

      formLayout: 'vertical'
    }
  },
  computed: {

    formItemLayout () {
      const { formLayout } = this
      return formLayout === 'horizontal' ? {
        labelCol: { span: 4 },
        wrapperCol: { span: 14 }
      } : {}
    },

    horizontalFormItemLayout () {
      return {
        labelCol: { span: 4 },
        wrapperCol: { span: 14 }
      }
    },
    buttonItemLayout () {
      const { formLayout } = this
      return formLayout === 'horizontal' ? {
        wrapperCol: { span: 14, offset: 4 }
      } : {}
    }
  },
  mounted () {
    this.getCITypes()
    this.getAttributes()
  },
  methods: {

    filterOption (input, option) {
      return (
        option.componentOptions.children[0].text.toLowerCase().indexOf(input.toLowerCase()) >= 0
      )
    },
    getCITypes () {
      getCITypes().then(res => {
        this.CITypes = res.ci_types
        this.CITypes.unshift({})
      })
    },

    getAttributes () {
      searchAttributes({ page_size: 10000 }).then(res => {
        this.allAttributes = res.attributes
      })
    },
    handleCreate () {
      this.drawerTitle = this.$t('ciType.newCIType')
      this.drawerVisible = true
    },
    onClose () {
      this.form.resetFields()
      this.drawerVisible = false
    },
    handleEdit (record) {
      this.drawerTitle = this.$t('ciType.editCIType')
      this.drawerVisible = true

      this.$nextTick(() => {
        this.form.setFieldsValue({
          id: record.id,
          alias: record.alias,
          name: record.name,
          unique_key: record.unique_id

        })
      })
    },

    handleDelete (record) {
      deleteCIType(record.id)
        .then(res => {
          this.$message.success(this.$t('tip.deleteSuccess'))
          this.getCITypes()
        })
        .catch(err => this.requestFailed(err))
    },

    handleSubmit (e) {
      e.preventDefault()
      this.form.validateFields((err, values) => {
        if (!err) {
          // eslint-disable-next-line no-console
          console.log('Received values of form: ', values)

          if (values.id) {
            this.updateCIType(values.id, values)
          } else {
            this.createCIType(values)
          }
        }
      })
    },
    createCIType (data) {
      createCIType(data)
        .then(res => {
          this.$message.success(this.$t('tip.addSuccess'))
          this.drawerVisible = false
          this.getCITypes()
        })
        .catch(err => this.requestFailed(err))
    },

    updateCIType (CITypeId, data) {
      updateCIType(CITypeId, data)
        .then(res => {
          this.$message.success(this.$t('tip.updateSuccess'))
          this.drawerVisible = false
          this.getCITypes()
        })
        .catch(err => this.requestFailed(err))
    },
    requestFailed (err) {
      const msg = ((err.response || {}).data || {}).message || this.$t('tip.requestFailed')
      this.$message.error(`${msg}`)
    }

  },
  props: {},
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

  .new-btn {
    background-color: #fff;
    border-radius: 2px;
    width: 100%;
    height: 7.5rem;
  }
  @media screen and (max-width: 900px) {
    .fold {
      width: 100%;
    }
  }
</style>
