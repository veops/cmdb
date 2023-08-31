<template>
  <div class="ops-setting-companyinfo" :style="{ height: `${windowHeight - 64}px` }">
    <a-form-model ref="infoData" :model="infoData" :label-col="labelCol" :wrapper-col="wrapperCol" :rules="rule">
      <SpanTitle>公司描述</SpanTitle>
      <a-form-model-item label="名称" prop="name">
        <a-input v-model="infoData.name" :disabled="!isEditable" />
      </a-form-model-item>
      <a-form-model-item label="描述">
        <a-input v-model="infoData.description" type="textarea" :disabled="!isEditable" />
      </a-form-model-item>
      <SpanTitle>公司地址</SpanTitle>
      <a-form-model-item label="国家/地区">
        <a-input v-model="infoData.country" :disabled="!isEditable" />
      </a-form-model-item>
      <a-form-model-item label="城市">
        <a-input v-model="infoData.city" :disabled="!isEditable" />
      </a-form-model-item>
      <a-form-model-item label="地址">
        <a-input v-model="infoData.address" :disabled="!isEditable" />
      </a-form-model-item>
      <a-form-model-item label="邮编">
        <a-input v-model="infoData.postCode" :disabled="!isEditable" />
      </a-form-model-item>
      <SpanTitle>联系方式</SpanTitle>
      <a-form-model-item label="网站">
        <a-input v-model="infoData.website" :disabled="!isEditable" />
      </a-form-model-item>
      <a-form-model-item label="电话号码" prop="phone">
        <a-input v-model="infoData.phone" :disabled="!isEditable" />
      </a-form-model-item>
      <a-form-model-item label="传真号码" prop="faxCode">
        <a-input v-model="infoData.faxCode" :disabled="!isEditable" />
      </a-form-model-item>
      <a-form-model-item label="电子邮箱" prop="email">
        <a-input v-model="infoData.email" :disabled="!isEditable" />
      </a-form-model-item>
      <SpanTitle>公司标识</SpanTitle>
      <a-form-model-item label="部署域名" prop="domainName">
        <a-input v-model="infoData.domainName" :disabled="!isEditable" />
      </a-form-model-item>
      <a-form-model-item label="公司logo">
        <a-space>
          <a-upload
            :disabled="!isEditable"
            name="avatar"
            list-type="picture-card"
            class="avatar-uploader"
            :show-upload-list="false"
            :customRequest="customRequest"
            :before-upload="beforeUpload"
            :style="{ width: '400px', height: '80px' }"
            accept=".png,.jpg,.jpeg"
          >
            <div
              class="ops-setting-companyinfo-upload-show"
              v-if="infoData.logoName"
              :style="{ width: '400px', height: '80px' }"
              @click="eidtImageOption.type = 'Logo'"
            >
              <img :src="`/api/common-setting/v1/file/${infoData.logoName}`" alt="avatar" />
              <a-icon
                v-if="isEditable"
                type="minus-circle"
                theme="filled"
                class="delete-icon"
                @click.stop="deleteLogo"
              />
            </div>
            <div v-else @click="eidtImageOption.type = 'Logo'">
              <a-icon type="plus" />
              <div class="ant-upload-text">上传</div>
            </div>
          </a-upload>

          <a-upload
            :disabled="!isEditable"
            name="avatar"
            list-type="picture-card"
            class="avatar-uploader"
            :show-upload-list="false"
            :customRequest="customRequest"
            :before-upload="beforeUpload"
            :style="{ width: '82px', height: '82px' }"
            accept=".png,.jpg,.jpeg"
          >
            <div
              class="ops-setting-companyinfo-upload-show"
              v-if="infoData.smallLogoName"
              :style="{ width: '82px', height: '82px' }"
              @click="eidtImageOption.type = 'SmallLogo'"
            >
              <img :src="`/api/common-setting/v1/file/${infoData.smallLogoName}`" alt="avatar" />
              <a-icon
                v-if="isEditable"
                type="minus-circle"
                theme="filled"
                class="delete-icon"
                @click.stop="deleteSmallLogo"
              />
            </div>
            <div v-else @click="eidtImageOption.type = 'SmallLogo'">
              <a-icon type="plus" />
              <div class="ant-upload-text">上传</div>
            </div>
          </a-upload>
        </a-space>
      </a-form-model-item>
      <a-form-model-item :wrapper-col="{ span: 14, offset: 3 }" v-if="isEditable">
        <a-button type="primary" @click="onSubmit"> 保存 </a-button>
        <a-button ghost type="primary" style="margin-left: 28px" @click="resetForm"> 重置 </a-button>
      </a-form-model-item>
    </a-form-model>
    <edit-image
      v-if="showEditImage"
      :show="showEditImage"
      :image="editImage"
      :title="eidtImageOption.title"
      :eidtImageOption="eidtImageOption"
      @save="submitImage"
      @close="showEditImage = false"
    />
  </div>
</template>

<script>
import { getCompanyInfo, postCompanyInfo, putCompanyInfo } from '@/api/company'
import { postImageFile } from '@/api/file'
import { mapMutations, mapState } from 'vuex'
import SpanTitle from '../components/spanTitle.vue'
import EditImage from '../components/EditImage.vue'
import { mixinPermissions } from '@/utils/mixin'
export default {
  name: 'CompanyInfo',
  mixins: [mixinPermissions],
  components: { SpanTitle, EditImage },
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
        logoName: '',
        smallLogoName: '',
      },
      rule: {
        name: [{ required: true, whitespace: true, message: '请输入名称', trigger: 'blur' }],
        phone: [
          {
            required: false,
            whitespace: true,
            pattern: new RegExp('^([0-9]|-)+$', 'g'),
            message: '请输入正确的电话号码',
            trigger: 'blur',
          },
        ],
        faxCode: [
          {
            required: false,
            whitespace: true,
            pattern: new RegExp('^([0-9]|-)+$', 'g'),
            message: '请输入正确的传真号码',
            trigger: 'blur',
          },
        ],
        email: [
          {
            required: false,
            whitespace: true,
            pattern: new RegExp('^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(.[a-zA-Z0-9-]+)*.[a-zA-Z0-9]{2,6}$', 'g'),
            message: '请输入正确的邮箱地址',
            trigger: 'blur',
          },
        ],
      },
      getId: -1,
      showEditImage: false,
      editImage: null,
      eidtImageOption: {
        type: 'Logo',
        fixedNumber: [15, 4],
        title: '编辑企业logo',
        previewWidth: '200px',
        previewHeight: '40px',
        autoCropWidth: 200,
        autoCropHeight: 40,
      },
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
    ...mapState({
      windowHeight: (state) => state.windowHeight,
    }),
    isEditable() {
      return this.hasDetailPermission('backend', '公司信息', ['update'])
    },
  },
  methods: {
    ...mapMutations(['SET_FILENAME', 'SET_SMALL_FILENAME']),
    deleteLogo() {
      this.infoData.logoName = ''
    },
    deleteSmallLogo() {
      this.infoData.smallLogoName = ''
    },
    async onSubmit() {
      this.$refs.infoData.validate(async (valid) => {
        if (valid) {
          if (this.getId === -1) {
            await postCompanyInfo(this.infoData)
          } else {
            await putCompanyInfo(this.getId, this.infoData)
          }
          this.SET_FILENAME(this.infoData.logoName)
          this.SET_SMALL_FILENAME(this.infoData.smallFileName)
          this.$message.success('保存成功')
        } else {
          this.$message.warning('检查您的输入是否正确!')
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
        logoName: '',
        smallLogoName: '',
      }
    },
    customRequest(file) {
      const reader = new FileReader()
      var self = this
      if (this.eidtImageOption.type === 'Logo') {
        this.eidtImageOption = {
          type: 'Logo',
          fixedNumber: [20, 4],
          title: '编辑企业logo',
          previewWidth: '200px',
          previewHeight: '40px',
          autoCropWidth: 200,
          autoCropHeight: 40,
        }
      } else if (this.eidtImageOption.type === 'SmallLogo') {
        this.eidtImageOption = {
          type: 'SmallLogo',
          fixedNumber: [4, 4],
          title: '编辑企业logo缩略图',
          previewWidth: '80px',
          previewHeight: '80px',
          autoCropWidth: 250,
          autoCropHeight: 250,
        }
      }
      reader.onload = function(e) {
        let result
        if (typeof e.target.result === 'object') {
          // 把Array Buffer转化为blob 如果是base64不需要
          result = window.URL.createObjectURL(new Blob([e.target.result]))
        } else {
          result = e.target.result
        }

        self.editImage = result
        self.showEditImage = true
      }
      reader.readAsDataURL(file.file)
    },
    submitImage(file) {
      postImageFile(file).then((res) => {
        if (res.file_name) {
          if (this.eidtImageOption.type === 'Logo') {
            this.infoData.logoName = res.file_name
          } else if (this.eidtImageOption.type === 'SmallLogo') {
            this.infoData.smallLogoName = res.file_name
          }
        } else {
        }
      })
    },

    beforeUpload(file) {
      const isLt2M = file.size / 1024 / 1024 < 2
      if (!isLt2M) {
        this.$message.error('图片大小不可超过2MB!')
      }
      return isLt2M
    },
  },
}
</script>

<style lang="less">
.ops-setting-companyinfo {
  padding-top: 15px;
  background-color: #fff;
  border-radius: 15px;
  overflow: auto;
  margin-bottom: -24px;
  .ops-setting-companyinfo-upload-show {
    position: relative;
    width: 290px;
    height: 100px;
    max-height: 100px;
    img {
      width: 100%;
      height: 100%;
    }

    .delete-icon {
      display: none;
    }
  }
  .ant-upload:hover .delete-icon {
    display: block;
    position: absolute;
    top: 5px;
    right: 5px;
    color: rgb(247, 85, 85);
  }
  .ant-form-item {
    margin-bottom: 10px;
  }
  .ant-form-item label {
    padding-right: 10px;
  }
  .avatar-uploader > .ant-upload {
    // max-width: 100px;
    max-height: 100px;
  }
  // .ant-upload.ant-upload-select-picture-card {
  //   width: 100%;
  //   > .ant-upload {
  //     padding: 0px;
  .ant-upload-picture-card-wrapper {
    height: 100px;
    .ant-upload.ant-upload-select-picture-card {
      width: 100%;
      height: 100%;
      margin: 0;
      > .ant-upload {
        padding: 0px;
      }
    }
  }
}
</style>
