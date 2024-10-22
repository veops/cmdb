<template>
  <div class="ops-setting-companyinfo">
    <a-form-model ref="infoData" :model="infoData" :label-col="labelCol" :wrapper-col="wrapperCol" :rules="rule">
      <SpanTitle>{{ $t('cs.companyInfo.spanCompany') }}</SpanTitle>
      <a-form-model-item :label="$t('cs.companyInfo.name')" prop="name">
        <a-input v-model="infoData.name" :disabled="!isEditable" />
      </a-form-model-item>
      <a-form-model-item :label="$t('cs.companyInfo.description')">
        <a-input v-model="infoData.description" type="textarea" :disabled="!isEditable" />
      </a-form-model-item>
      <SpanTitle>{{ $t('cs.companyInfo.spanAddress') }}</SpanTitle>
      <a-form-model-item :label="$t('cs.companyInfo.country')">
        <a-input v-model="infoData.country" :disabled="!isEditable" />
      </a-form-model-item>
      <a-form-model-item :label="$t('cs.companyInfo.city')">
        <a-input v-model="infoData.city" :disabled="!isEditable" />
      </a-form-model-item>
      <a-form-model-item :label="$t('cs.companyInfo.address')">
        <a-input v-model="infoData.address" :disabled="!isEditable" />
      </a-form-model-item>
      <a-form-model-item :label="$t('cs.companyInfo.postcode')">
        <a-input v-model="infoData.postCode" :disabled="!isEditable" />
      </a-form-model-item>
      <SpanTitle>{{ $t('cs.companyInfo.spanContract') }}</SpanTitle>
      <a-form-model-item :label="$t('cs.companyInfo.website')">
        <a-input v-model="infoData.website" :disabled="!isEditable" />
      </a-form-model-item>
      <a-form-model-item :label="$t('cs.companyInfo.phone')" prop="phone">
        <a-input v-model="infoData.phone" :disabled="!isEditable" />
      </a-form-model-item>
      <a-form-model-item :label="$t('cs.companyInfo.faxCode')" prop="faxCode">
        <a-input v-model="infoData.faxCode" :disabled="!isEditable" />
      </a-form-model-item>
      <a-form-model-item :label="$t('cs.companyInfo.email')" prop="email">
        <a-input v-model="infoData.email" :disabled="!isEditable" />
      </a-form-model-item>
      <SpanTitle>{{ $t('cs.companyInfo.spanLogo') }}</SpanTitle>
      <a-form-model-item :label="$t('cs.companyInfo.domainName')" prop="domainName">
        <a-input v-model="infoData.domainName" :disabled="!isEditable" />
      </a-form-model-item>
      <a-form-model-item :wrapper-col="{ span: 14, offset: 3 }" v-if="isEditable">
        <a-button type="primary" @click="onSubmit"> {{ $t('save') }}</a-button>
        <a-button ghost type="primary" style="margin-left: 28px" @click="resetForm"> {{ $t('reset') }}</a-button>
      </a-form-model-item>
    </a-form-model>
  </div>
</template>

<script>
import { mapMutations } from 'vuex'
import { getCompanyInfo, postCompanyInfo, putCompanyInfo } from '@/api/company'
import SpanTitle from '../components/spanTitle.vue'
import { mixinPermissions } from '@/utils/mixin'

export default {
  name: 'CompanyInfo',
  mixins: [mixinPermissions],
  components: { SpanTitle },
  data() {
    return {
      labelCol: { span: 3 },
      wrapperCol: { span: 10 },
      infoData: {
        name: '',
        description: '',
        address: '',
        city: '',
        postCode: '',
        country: '',
        website: '',
        phone: '',
        faxCode: '',
        email: '',
        domainName: '',
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
      this.SET_COMPANY_NAME(res?.info?.name || '')
    }
  },
  computed: {
    isEditable() {
      return this.hasDetailPermission('backend', '公司信息', ['update'])
    },
    rule() {
      return {
        name: [{ required: true, whitespace: true, message: this.$t('cs.companyInfo.nameValidate'), trigger: 'blur' }],
        phone: [
          {
            required: false,
            whitespace: true,
            pattern: new RegExp('^([0-9]|-)+$', 'g'),
            message: this.$t('cs.companyInfo.phoneValidate'),
            trigger: 'blur',
          },
        ],
        faxCode: [
          {
            required: false,
            whitespace: true,
            pattern: new RegExp('^([0-9]|-)+$', 'g'),
            message: this.$t('cs.companyInfo.faxCodeValidate'),
            trigger: 'blur',
          },
        ],
        email: [
          {
            required: false,
            whitespace: true,
            pattern: new RegExp('^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(.[a-zA-Z0-9-]+)*.[a-zA-Z0-9]{2,6}$', 'g'),
            message: this.$t('cs.companyInfo.emailValidate'),
            trigger: 'blur',
          },
        ],
      }
    },
  },
  methods: {
    ...mapMutations(['SET_COMPANY_NAME']),
    async onSubmit() {
      this.$refs.infoData.validate(async (valid) => {
        if (valid) {
          if (this.getId === -1) {
            await postCompanyInfo(this.infoData)
          } else {
            await putCompanyInfo(this.getId, this.infoData)
          }
          this.SET_COMPANY_NAME(this.infoData.name || '')
          this.$message.success(this.$t('saveSuccess'))
        } else {
          this.$message.warning(this.$t('cs.companyInfo.checkInputCorrect'))
          return false
        }
      })
    },
    resetForm() {
      this.infoData = {
        name: '',
        description: '',
        address: '',
        city: '',
        postCode: '',
        country: '',
        website: '',
        phone: '',
        faxCode: '',
        email: '',
        domainName: '',
      }
    },
  },
}
</script>

<style lang="less">
.ops-setting-companyinfo {
  padding: 20px;
  background-color: #fff;
  border-radius: @border-radius-box;
  overflow: auto;
  margin-bottom: -24px;
  height: calc(100vh - 64px);

  .ant-form-item {
    margin-bottom: 10px;
  }
}
</style>
