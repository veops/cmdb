<template>
  <div class="acl-secret-key">
    <a-form-model
      ref="secretKeyForm"
      :model="displayForm"
      :rules="rules"
      :label-col="{ span: 6 }"
      :wrapper-col="{ span: 12 }"
    >
      <a-form-model-item label="Key" prop="key">
        <a-input disabled v-model="displayForm.key" />
      </a-form-model-item>
      <a-form-model-item label="Secret" prop="secret">
        <a-input disabled v-model="displayForm.secret" />
      </a-form-model-item>
      <a-form-model-item label=" " :colon="false">
        <a-space>
          <a-button type="primary" @click="changeVisible">{{ !visible ? $t('view') : $t('hide') }}</a-button>
          <a-button type="danger" ghost @click="handleSumbit">{{ $t('reset') }}</a-button>
          <!-- <a-button @click="handleCancel">{{ $t('cancel') }}</a-button> -->
        </a-space>
      </a-form-model-item>
    </a-form-model>
  </div>
</template>

<script>
import { getSecret, updateSecret } from '../api/secretKey'
export default {
  name: 'SecretKey',
  data() {
    return {
      form: {
        key: '',
        secret: '',
      },
      rules: {
        key: [{ required: false, message: 'key is required' }],
        secret: [{ required: false, message: 'secret is required' }],
      },
      visible: false,
    }
  },
  computed: {
    displayForm() {
      return {
        key: this.visible ? this.form.key : this.form.key.replace(/./g, '*'),
        secret: this.visible ? this.form.secret : this.form.secret.replace(/./g, '*'),
      }
    },
  },
  mounted() {
    this.getOriginSecret()
  },
  methods: {
    getOriginSecret() {
      getSecret().then((res) => {
        const { key, secret } = res
        this.form = { key, secret }
      })
    },
    handleSumbit() {
      const that = this
      this.$confirm({
        title: that.$t('reset'),
        content: that.$t('acl.confirmResetSecret'),
        onOk() {
          that.$refs.secretKeyForm.validate((valid) => {
            if (valid) {
              updateSecret().then((res) => {
                that.$message.success(that.$t('operateSuccess'))
                const { key, secret } = res
                that.form = { key, secret }
              })
            }
          })
        },
      })
    },
    handleCancel() {
      this.getOriginSecret()
    },
    changeVisible() {
      this.visible = !this.visible
    },
  },
}
</script>

<style lang="less">
.acl-secret-key {
  background-color: #fff;
  padding: 24px;
  border-radius: 15px;
  height: calc(100% + 24px);
  .ant-input[disabled] {
    color: rgba(0, 0, 0, 0.5);
  }
}
</style>
