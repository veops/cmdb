<template>
  <div class="ops-setting-notice-basic">
    <a-form-model ref="infoData" :model="infoData" :label-col="labelCol" :wrapper-col="wrapperCol">
      <a-form-model-item :label="$t('cs.companyInfo.messenger')" prop="messenger">
        <a-input v-model="infoData.messenger" :disabled="!isEditable" />
      </a-form-model-item>
      <a-form-model-item :wrapper-col="{ span: 14, offset: 3 }" v-if="isEditable">
        <a-button type="primary" @click="onSubmit"> {{ $t('save') }}</a-button>
        <a-button ghost type="primary" style="margin-left: 28px" @click="resetForm"> {{ $t('reset') }}</a-button>
      </a-form-model-item>
    </a-form-model>
  </div>
</template>

<script>
import { getCompanyInfo, postCompanyInfo, putCompanyInfo } from '@/api/company'
import { mixinPermissions } from '@/utils/mixin'

export default {
  name: 'CompanyInfo',
  mixins: [mixinPermissions],
  data() {
    return {
      labelCol: { span: 3 },
      wrapperCol: { span: 10 },
      infoData: {
        messenger: '',
      },
      getId: -1,
    }
  },
  async mounted() {
    const res = await getCompanyInfo()
    if (!res.id) {
      this.getId = -1
    } else {
      this.infoData = res.info
      this.getId = res.id
    }
  },
  computed: {
    isEditable() {
      return this.hasDetailPermission('backend', '公司信息', ['update'])
    },
  },
  methods: {
    async onSubmit() {
      this.$refs.infoData.validate(async (valid) => {
        if (valid) {
          if (this.getId === -1) {
            await postCompanyInfo(this.infoData)
          } else {
            await putCompanyInfo(this.getId, this.infoData)
          }
          this.$message.success(this.$t('saveSuccess'))
        } else {
          this.$message.warning(this.$t('cs.companyInfo.checkInputCorrect'))
          return false
        }
      })
    },
    resetForm() {
      this.infoData = {
        messenger: '',
      }
    },
  },
}
</script>

<style lang="less">
.ops-setting-notice-basic {
  padding-top: 20px;
  background-color: #fff;
  border-radius: @border-radius-box;
  overflow: auto;
  margin-bottom: -24px;
  height: calc(100vh - 64px);
}
</style>
