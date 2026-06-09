<template>
  <a-modal
    v-model="visible"
    :title="$t('cmdb.ci.qrcodeBatchTitle')"
    width="800px"
    :footer="null"
    :maskClosable="true"
  >
    <p class="qrcode-batch-tip">{{ $t('cmdb.ci.qrcodeBatchTip') }}</p>

    <div v-if="qrcodeList.length === 0 && !generating" class="qrcode-batch-empty">
      <a-empty :description="$t('cmdb.ci.qrcodeBatchEmpty')" />
    </div>

    <div v-if="generating" class="qrcode-batch-generating">
      <a-spin />
      <span>正在生成 {{ generatedCount }} / {{ totalCount }} ...</span>
    </div>

    <div v-if="qrcodeList.length" class="qrcode-batch-grid" ref="qrcodeGrid">
      <div
        v-for="item in qrcodeList"
        :key="item.ciId"
        class="qrcode-batch-item"
      >
        <canvas :ref="'qrcode-' + item.ciId"></canvas>
        <p class="qrcode-batch-item-label">{{ item.label }}</p>
        <p class="qrcode-batch-item-id">CI ID: {{ item.ciId }}</p>
      </div>
    </div>

    <div class="qrcode-batch-actions" v-if="qrcodeList.length">
      <a-button type="primary" @click="downloadAll">
        <a-icon type="download" /> {{ $t('cmdb.ci.qrcodeDownload') }}
      </a-button>
      <a-button @click="printAll">
        <a-icon type="printer" /> {{ $t('cmdb.ci.printQRCode') }}
      </a-button>
    </div>
  </a-modal>
</template>

<script>
import QRCode from 'qrcode'

export default {
  name: 'QRCodeBatchExport',
  data() {
    return {
      visible: false,
      ciList: [],
      qrcodeList: [],
      generating: false,
      generatedCount: 0,
      totalCount: 0
    }
  },
  methods: {
    open(ciList) {
      if (!ciList || !ciList.length) {
        this.$message.warning(this.$t('cmdb.ci.qrcodeBatchEmpty'))
        return
      }
      this.ciList = ciList
      this.qrcodeList = []
      this.visible = true
      this.$nextTick(() => {
        this.generateAll()
      })
    },
    async generateAll() {
      this.generating = true
      this.generatedCount = 0
      this.totalCount = this.ciList.length

      const qrcodeList = []
      for (const ci of this.ciList) {
        const mobileUrl = `${window.location.origin}/cmdb/mobile/${ci.typeId}/${ci.ciId}`
        qrcodeList.push({
          ciId: ci.ciId,
          typeId: ci.typeId,
          label: ci.label || ci.name || `CI ${ci.ciId}`,
          url: mobileUrl
        })
      }

      this.qrcodeList = qrcodeList
      await this.$nextTick()

      for (const item of this.qrcodeList) {
        const canvasRef = this.$refs['qrcode-' + item.ciId]
        const canvas = Array.isArray(canvasRef) ? canvasRef[0] : canvasRef
        if (canvas) {
          try {
            await QRCode.toCanvas(canvas, item.url, {
              width: 150,
              margin: 1,
              color: { dark: '#000000', light: '#ffffff' }
            })
          } catch (e) {
            console.error('QRCode generate failed for CI', item.ciId, e)
          }
        }
        this.generatedCount++
      }

      this.generating = false
    },
    downloadAll() {
      const grid = this.$refs.qrcodeGrid
      if (!grid) return

      const link = document.createElement('a')
      link.download = 'cmdb-qrcodes-batch.png'

      import('html2canvas').then(({ default: html2canvas }) => {
        html2canvas(grid, {
          backgroundColor: '#ffffff',
          scale: 2
        }).then((canvas) => {
          link.href = canvas.toDataURL('image/png')
          link.click()
        })
      }).catch(() => {
        this.$message.warning(this.$t('cmdb.ci.copyFailed'))
      })
    },
    printAll() {
      const grid = this.$refs.qrcodeGrid
      if (!grid) return

      const printWindow = window.open('', '_blank', 'width=800,height=600')
      if (!printWindow) {
        this.$message.warning(this.$t('cmdb.ci.copyFailed'))
        return
      }

      const content = grid.innerHTML
      printWindow.document.write(`
        <html>
          <head>
            <title>CMDB QR Codes</title>
            <style>
              body { font-family: Arial, sans-serif; padding: 20px; }
              .qrcode-batch-grid { display: flex; flex-wrap: wrap; gap: 20px; justify-content: center; }
              .qrcode-batch-item { text-align: center; width: 170px; }
              .qrcode-batch-item-label { font-size: 12px; margin: 4px 0 2px; word-break: break-all; }
              .qrcode-batch-item-id { font-size: 11px; color: #999; margin: 0; }
              @media print {
                .qrcode-batch-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
                .qrcode-batch-item { page-break-inside: avoid; }
              }
            </style>
          </head>
          <body>
            <div class="qrcode-batch-grid">${content}</div>
          </body>
        </html>
      `)
      printWindow.document.close()
      setTimeout(() => {
        printWindow.print()
        printWindow.close()
      }, 500)
    }
  }
}
</script>

<style lang="less" scoped>
.qrcode-batch-tip {
  color: rgba(0, 0, 0, 0.45);
  font-size: 13px;
  margin-bottom: 16px;
}

.qrcode-batch-empty {
  padding: 20px 0;
}

.qrcode-batch-generating {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 40px 0;
  color: #999;
}

.qrcode-batch-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  justify-content: center;
  padding: 8px 0;
}

.qrcode-batch-item {
  text-align: center;
  width: 160px;
  padding: 12px 8px;
  border: 1px solid #f0f0f0;
  border-radius: 8px;
  background: #fff;
}

.qrcode-batch-item-label {
  font-size: 12px;
  color: #333;
  margin: 6px 0 2px;
  word-break: break-all;
  max-width: 140px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.qrcode-batch-item-id {
  font-size: 11px;
  color: #bbb;
  margin: 0;
}

.qrcode-batch-actions {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #f0f0f0;
}
</style>
