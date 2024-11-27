<template>
  <a-modal
    :visible="visible"
    :okText="$t('cmdb.dcim.toChange')"
    :width="350"
    @ok="handleOk"
    @cancel="handleCancel"
  >
    <div class="abnormal-modal-title">
      <a-icon
        type="info-circle"
        theme="filled"
        class="abnormal-modal-title-icon"
      />
      <span class="abnormal-modal-title-text">
        {{ $t('cmdb.dcim.unitAbnormal') }}
      </span>
    </div>

    <div class="abnormal-modal-content">
      <div class="abnormal-modal-content-row">
        <span
          v-for="(item, index) in abnormalList"
          :key="item.id"
        >
          {{ item.CITypeName }}
          <span class="abnormal-modal-content-name" >
            {{ item.name }}
          </span>
          <span
            v-if="index !== abnormalList.length - 1"
          >
            {{ $t('cmdb.dcim.abnormalModalTip1') }}
          </span>
        </span>
        <span>{{ $t('cmdb.dcim.abnormalModalTip2') }}</span>
      </div>
      <div class="abnormal-modal-content-row">
        {{ $t('cmdb.dcim.abnormalModalTip3') }}
      </div>
    </div>

    <a-radio-group
      v-model="currentSelect"
    >
      <a-radio
        v-for="(item) in abnormalList"
        :value="item.id"
        :key="item.id"
      >
        {{ item.name }}
      </a-radio>
    </a-radio-group>
  </a-modal>
</template>

<script>
export default {
  name: 'AbnormalModal',
  data() {
    return {
      visible: false,
      abnormalList: [],
      currentSelect: undefined,
    }
  },
  methods: {
    open(data) {
      this.visible = true

      const abnormalList = [data]
      if (data?.abnormalList?.length) {
        abnormalList.push(...data.abnormalList)
      }
      this.abnormalList = abnormalList

      this.currentSelect = abnormalList?.[0]?.id ?? undefined
    },

    handleCancel() {
      this.currentSelect = undefined
      this.abnormalList = []
      this.visible = false
    },

    handleOk() {
      if (!this.currentSelect) {
        return
      }

      const device = this.abnormalList.find((item) => item.id === this.currentSelect)
      this.$emit('ok', device)

      this.handleCancel()
    }
  }
}
</script>

<style lang="less" scoped >
.abnormal-modal-title {
  display: flex;
  align-items: center;

  &-icon {
    font-size: 18px;
    color: #FF7D00;
  }

  &-text {
    margin-left: 8px;
    font-size: 16px;
    font-weight: 700;
    color: #1D2129;
  }
}

.abnormal-modal-content {
  font-size: 14px;
  font-weight: 400;
  line-height: 22px;
  margin: 9px 0px;
  color: #1D2129;

  &-name {
    color: #2F54EB;
  }
}
</style>
