<template>
  <div class="attr-ad-tabs">
    <div
      v-for="item in adCITypeList"
      :key="item.id"
      :class="['attr-ad-tab', currentTab === item.id ? 'attr-ad-tab_active' : '']"
      @click="changeTab(item.id)"
    >
      <img
        v-if="item.icon.id && item.icon.url"
        :src="`/api/common-setting/v1/file/${item.icon.url}`"
        class="attr-ad-tab-icon"
      />
      <ops-icon
        v-else-if="item.icon.name"
        :type="item.icon.name || 'caise-chajian'"
        :style="{ color: item.icon.color }"
        class="attr-ad-tab-icon"
      />
      <a-input
        v-if="nameEditId === item.id"
        v-model="nameEditValue"
        :ref="`name-edit-${item.id}`"
        size="small"
        :autofocus="true"
        @blur="changeAlias(item.isClient || false)"
      />
      <span v-else class="attr-ad-tab-name">
        {{ item.extra_option && item.extra_option.alias ? item.extra_option.alias : getADCITypeParam(item.adr_id) }}
      </span>
      <a-icon
        type="edit"
        class="attr-ad-tab-edit"
        @click="(e) => openNameEdit(e, item)"
      />
      <a-icon
        type="delete"
        class="attr-ad-tab-delete"
        @click="(e) => deleteADT(e, item)"
      />
    </div>
    <a-icon
      type="plus-circle"
      class="attr-ad-tabs-add"
      @click="clickAdd"
    ></a-icon>
  </div>
</template>

<script>
export default {
  name: 'AttrADTabs',
  props: {
    currentTab: {
      type: [String, Number],
      default: ''
    },
    adCITypeList: {
      type: Array,
      default: () => [],
    },
    getADCITypeParam: {
      type: Function,
      default: () => ''
    }
  },
  data() {
    return {
      nameEditId: '',
      nameEditValue: '',
    }
  },
  methods: {
    changeTab(id) {
      this.$emit('changeTab', id)
    },
    openNameEdit(e, item) {
      e.preventDefault()
      e.stopPropagation()
      this.nameEditId = item.id
      if (item?.extra_option?.alias) {
        this.nameEditValue = item.extra_option.alias
      }
      this.$nextTick(() => {
        if (this.$refs?.[`name-edit-${item.id}`]?.[0]) {
          this.$refs[`name-edit-${item.id}`][0].focus()
        }
      })
    },
    changeAlias(isClient) {
      this.$emit('changeAlias', {
        id: this.nameEditId,
        value: this.nameEditValue,
        isClient
      })
      this.$nextTick(() => {
        this.nameEditId = ''
        this.nameEditValue = ''
      })
    },
    deleteADT(e, item) {
      e.preventDefault()
      e.stopPropagation()
      this.$emit('deleteADT', item)
    },
    clickAdd() {
      this.$emit('clickAdd')
    }
  }
}
</script>

<style lang="less" scoepd>
.attr-ad-tabs {
  display: flex;
  align-items: center;
  width: 100%;
  overflow-x: auto;
  padding-bottom: 10px;

  .attr-ad-tab {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 8px 24px;
    margin-right: 12px;
    background-color: @primary-color_7;
    cursor: pointer;
    flex-shrink: 0;

    &-name {
      font-weight: 400;
      font-size: 12px;
    }

    &-icon {
      font-size: 12px;
      width: 12px;
      height: 12px;
      margin-right: 4px;
    }

    &-edit {
      display: none;
      font-size: 10px;
      color: @text-color_4;
      margin-left: 4px;
    }

    &-delete {
      display: none;
      font-size: 10px;
      color: @func-color_1;
      margin-left: 6px;
    }

    &_active {
      border: solid 1px @primary-color_8;
      background-color: @primary-color_6;

      .attr-ad-tab-name {
        color: @primary-color;
      }
    }

    &:hover {
      .attr-ad-tab-edit {
        display: inline-block;
      }
      .attr-ad-tab-delete {
        display: inline-block;
      }
    }
  }

  &-add {
    padding: 11px;
    background-color: @primary-color_7;
    font-size: 12px;
    color: @text-color_4;
  }
}
</style>
