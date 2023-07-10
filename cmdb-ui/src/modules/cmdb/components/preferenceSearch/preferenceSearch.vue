<template>
  <div>
    <span :style="{ marginRight: '10px' }">
      <a-input
        v-if="inputVisible"
        ref="input"
        type="text"
        size="small"
        :style="{ width: '78px' }"
        v-model="inputValue"
        @blur="handleInputConfirm"
        @keyup.enter="handleInputConfirm"
      />
      <a-button v-else type="primary" size="small" ghost @click="showInput">保存筛选条件</a-button>
    </span>
    <template v-for="(item, index) in preferenceSearchList.slice(0, 3)">
      <span
        v-if="item.name.length > 6"
        class="preference-search-tag"
        :key="`${item.id}_${index}`"
        :style="{
          backgroundColor: item.id === currentPreferenceSearch ? '#2f54eb' : '',
          color: item.id === currentPreferenceSearch ? '#fff' : '',
        }"
      >
        <a-tooltip :title="item.name">
          <span @click="clickPreferenceSearch(item)">{{ `${item.name.slice(0, 6)}...` }}</span>
        </a-tooltip>
        <a-popconfirm title="确认删除？" @confirm="deletePreferenceSearch(item)">
          <a-icon type="close" />
        </a-popconfirm>
      </span>
      <span
        v-else
        :key="`${item.id}_${index}`"
        class="preference-search-tag"
        :style="{
          backgroundColor: item.id === currentPreferenceSearch ? '#2f54eb' : '#fafafa',
          color: item.id === currentPreferenceSearch ? '#fff' : '#000000a6',
        }"
      >
        <span @click="clickPreferenceSearch(item)">{{ item.name }}</span>
        <a-popconfirm title="确认删除？" @confirm="deletePreferenceSearch(item)">
          <a-icon type="close" />
        </a-popconfirm>
      </span>
    </template>
    <a-dropdown v-if="preferenceSearchList.length > 3" v-model="visible">
      <a @click="(e) => e.preventDefault()"><a-icon type="down" /> </a>
      <a-menu slot="overlay">
        <a-menu-item
          v-for="(item, index) in preferenceSearchList.slice(3)"
          :key="`${item.id}_${index}`"
          :style="{
            display: 'flex',
            flexDirection: 'row',
            justifyContent: 'space-between',
            alignItems: 'center',
            fontSize: '12px',
          }"
        >
          <div
            @click="clickPreferenceSearch(item, index, true)"
            :style="{
              display: 'inline-block',
              width: '120px',
              overflow: 'hidden',
              textOverflow: 'ellipsis',
              whiteSpace: 'nowrap',
            }"
            :title="item.name"
          >
            {{ item.name }}
          </div>
          <a-popconfirm
            title="确认删除？"
            :getPopupContainer="(trigger) => trigger.parentElement"
            placement="left"
            @confirm="
              (e) => {
                e.preventDefault()
                e.stopPropagation()
                deletePreferenceSearch(item)
              }
            "
          >
            <a-icon class="preference-search-delete" type="close" />
          </a-popconfirm>
        </a-menu-item>
      </a-menu>
    </a-dropdown>
  </div>
</template>

<script>
import _ from 'lodash'
import { getPreferenceSearch, savePreferenceSearch, deletePreferenceSearch } from '../../api/preference'

export default {
  name: 'PreferenceSearch',
  data() {
    return {
      inputValue: '',
      inputVisible: false,
      preferenceSearchList: [],
      currentPreferenceSearch: null,
      visible: false,
    }
  },
  inject: ['filterCompPreferenceSearch'],
  computed: {
    inject_filterCompPreferenceSearch() {
      return this.filterCompPreferenceSearch()
    },
  },
  watch: {
    inject_filterCompPreferenceSearch: {
      immediate: true,
      deep: true,
      handler(newValue) {
        this.getPreferenceSearchList()
      },
    },
  },
  methods: {
    getPreferenceSearchList() {
      getPreferenceSearch({ ...this.inject_filterCompPreferenceSearch }).then((res) => {
        if (!this.inject_filterCompPreferenceSearch) {
          this.preferenceSearchList = res.filter((item) => !item.type_id && !item.ptv_id && !item.prv_id)
        } else {
          this.preferenceSearchList = res
        }
      })
    },
    showInput() {
      this.inputVisible = true
      this.$nextTick(() => {
        setTimeout(() => {
          this.$refs.input.focus()
        }, 100)
      })
    },
    handleInputConfirm() {
      this.$emit('getQAndSort')
    },
    savePreference({ fuzzySearch, expression, currenCiType = undefined }) {
      if (this.inputValue) {
        savePreferenceSearch({
          ...this.filterCompPreferenceSearch(),
          name: this.inputValue,
          option: { fuzzySearch, expression, currenCiType },
        }).then(() => {
          this.getPreferenceSearchList()
        })
      }
      this.inputValue = ''
      this.inputVisible = false
    },
    deletePreferenceSearch(item) {
      deletePreferenceSearch(item.id).then((res) => {
        this.getPreferenceSearchList()
      })
    },
    clickPreferenceSearch(item, index, isGotoFirst = false) {
      if (isGotoFirst) {
        const _preferenceSearchList = _.cloneDeep(this.preferenceSearchList)
        const spliceList = _preferenceSearchList.splice(index + 3, 1)
        _preferenceSearchList.unshift(_.cloneDeep(spliceList[0]))
        this.preferenceSearchList = _preferenceSearchList
      }
      this.currentPreferenceSearch = item.id
      this.$emit('setParamsFromPreferenceSearch', item)
    },
  },
}
</script>

<style lang="less" scoped>
.preference-search-tag {
  cursor: pointer;
  border-radius: 5px;
  border: none;
  display: inline-block;
  padding: 0 7px;
  margin-right: 8px;
  > span {
    margin-right: 4px;
  }
  > i {
    font-size: 12px;
  }
}
.preference-search-delete {
  color: #a9a9a9;
  &:hover {
    color: #626262;
  }
}
</style>
