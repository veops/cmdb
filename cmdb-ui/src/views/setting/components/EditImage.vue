<template>
  <a-modal
    class="ops-modal"
    v-loading="loading"
    :title="title"
    width="600px"
    :append-to-body="true"
    :close-on-click-modal="false"
    :visible.sync="showDialog"
    @cancel="hiddenView"
  >
    <div class="ops-modal-cropper-box">
      <vueCropper
        ref="cropper"
        :can-move="true"
        :auto-crop="true"
        :fixed="true"
        :img="cropperImg"
        output-type="png"
        @realTime="realTime"
        v-bind="eidtImageOption"
      />
      <div class="ops-modal-preview">
        <div class="ops-modal-preview-name">预览</div>
        <img
          :style="{
            width: eidtImageOption.previewWidth,
            height: eidtImageOption.previewHeight,
            border: '1px solid #f2f2f2',
          }"
          :src="previewImg"
          class="ops-modal-preview-img"
        />
      </div>
    </div>

    <div slot="footer" class="ops-modal-dialog-footer">
      <a-button type="primary" @click="submitImage()">确定</a-button>
    </div>
  </a-modal>
</template>
<script type="text/javascript">
import { VueCropper } from 'vue-cropper'

export default {
  name: 'EditImage', // 处理头像
  components: {
    VueCropper,
  },
  props: {
    title: {
      type: String,
      default: '编辑头像',
    },
    show: {
      type: Boolean,
      default: false,
    },
    image: {
      type: String,
      default: '',
    },
    eidtImageOption: {
      type: Object,
      default: () => {},
    },
  },
  data() {
    return {
      loading: false,
      showDialog: false,
      cropperImg: '',
      previewImg: '',
    }
  },
  computed: {},
  watch: {
    show: {
      handler(val) {
        this.showDialog = val
      },
      deep: true,
      immediate: true,
    },
    image: function(val) {
      this.cropperImg = val
    },
  },
  mounted() {
    this.cropperImg = this.image
  },
  methods: {
    realTime(data) {
      this.$refs.cropper.getCropData((cropperData) => {
        this.previewImg = cropperData
      })
    },
    submitImage() {
      // 获取截图的blob数据
      this.$refs.cropper.getCropBlob((data) => {
        const form = new FormData()
        form.append('file', data)
        this.$emit('save', form)
        this.hiddenView()
      })
    },
    hiddenView() {
      this.$emit('close')
    },
  },
}
</script>
<style lang="less" scoped>
.ops-modal {
  .ops-modal-cropper-box {
    position: relative;
    width: 300px;
    height: 300px;
  }

  .ops-modal-preview {
    position: absolute;
    bottom: 0;
    left: 325px;
    .ops-modal-preview-name {
      margin-bottom: 8px;
      font-size: 13px;
      color: #666;
    }
    .ops-modal-preview-img {
      display: block;
    }
  }

  .ops-modal-content {
    position: relative;
    padding: 0 30px;
  }
}
</style>
