<template>
  <span>
    <a @click="showQRCode" class="qrcode-btn" :style="{ marginRight: '12px' }">
      <a-icon type="qrcode" />
      {{ $t('cmdb.ci.qrcode') }}
    </a>

    <a-modal
      v-model="visible"
      :title="$t('cmdb.ci.qrcodeTitle')"
      :footer="null"
      width="360px"
      :maskClosable="true"
      centered
    >
      <div class="qrcode-modal-content">
        <p class="qrcode-modal-tip">{{ $t('cmdb.ci.qrcodeTip') }}</p>
        <div class="qrcode-canvas-wrapper">
          <canvas ref="qrcodeCanvas"></canvas>
        </div>
        <p class="qrcode-modal-url">{{ mobileUrl }}</p>
        <a-space class="qrcode-modal-actions">
          <a-button type="primary" size="small" @click="downloadQRCode">
            <a-icon type="download" /> {{ $t('cmdb.ci.qrcodeDownload') }}
          </a-button>
          <a-button size="small" @click="copyMobileUrl">
            <a-icon type="copy" /> {{ $t('copy') }}
          </a-button>
        </a-space>
      </div>
    </a-modal>
  </span>
</template>

<script>
import QRCode from 'qrcode'

export default {
  name: 'QRCodeButton',
  props: {
    typeId: {
      required: false,
      default: null,
      validator(value) {
        return value === null || typeof value === 'number' || typeof value === 'string'
      }
    },
    ciId: {
      required: false,
      default: null,
      validator(value) {
        return value === null || typeof value === 'number' || typeof value === 'string'
      }
    }
  },
  data() {
    return {
      visible: false
    }
  },
  computed: {
    hasValidId() {
      return this.typeId !== null && this.typeId !== undefined && this.ciId !== null && this.ciId !== undefined
    },
    mobileUrl() {
      if (!this.hasValidId) {
        return ''
      }
      const origin = window.location.origin
      return `${origin}/cmdb/mobile/${this.typeId}/${this.ciId}`
    }
  },
  methods: {
    async showQRCode() {
      if (!this.hasValidId) {
        return
      }
      this.visible = true
      this.$nextTick(() => {
        this.generateQRCode()
      })
    },
    async generateQRCode() {
      const canvas = this.$refs.qrcodeCanvas
      if (!canvas) return
      try {
        await QRCode.toCanvas(canvas, this.mobileUrl, {
          width: 220,
          margin: 1,
          color: {
            dark: '#000000',
            light: '#ffffff'
          }
        })
      } catch (e) {
        console.error('QRCode generate failed:', e)
      }
    },
    downloadQRCode() {
      const canvas = this.$refs.qrcodeCanvas
      if (!canvas || !this.hasValidId) return
      const link = document.createElement('a')
      link.download = `cmdb-ci-${this.ciId}-qrcode.png`
      link.href = canvas.toDataURL('image/png')
      link.click()
    },
    copyMobileUrl() {
      if (!this.hasValidId) {
        return
      }
      this.$copyText(this.mobileUrl)
        .then(() => {
          this.$message.success(this.$t('copySuccess'))
        })
        .catch(() => {
          this.$message.error(this.$t('cmdb.ci.copyFailed'))
        })
    }
  }
}
</script>

<style lang="less" scoped>
.qrcode-btn {
  color: rgba(0, 0, 0, 0.65);
  &:hover {
    color: @primary-color;
  }
}

.qrcode-modal-content {
  text-align: center;
}

.qrcode-modal-tip {
  color: rgba(0, 0, 0, 0.45);
  font-size: 13px;
  margin-bottom: 16px;
}

.qrcode-canvas-wrapper {
  display: flex;
  justify-content: center;
  margin-bottom: 12px;
}

.qrcode-modal-url {
  color: rgba(0, 0, 0, 0.45);
  font-size: 12px;
  word-break: break-all;
  margin-bottom: 16px;
  padding: 0 12px;
}

.qrcode-modal-actions {
  display: flex;
  justify-content: center;
}
</style>
