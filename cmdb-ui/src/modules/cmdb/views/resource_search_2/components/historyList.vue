<template>
  <div class="history-list">
    <div
      class="history-recent"
      v-if="recentList.length"
    >
      <div class="history-title">
        <a-icon type="eye" class="history-title-icon" />
        <div class="history-title-text">{{ $t('cmdb.ciType.recentSearch') }}</div>

        <a-popconfirm
          :title="$t('cmdb.ciType.confirmClear')"
          placement="topRight"
          @confirm="clearRecent"
        >
          <a-tooltip :title="$t('clear')" >
            <a-icon
              type="delete"
              class="history-title-clear"
            />
          </a-tooltip>
        </a-popconfirm>
      </div>
      <div class="recent-list">
        <div
          v-for="(item) in recentList.slice(0, 10)"
          :key="item.id"
          class="recent-list-item"
          @click="clickRecent(item.option)"
        >
          <div class="recent-list-item-text">
            {{ getRecentSearchText(item.option) }}
          </div>
          <a-icon
            type="close"
            class="recent-list-item-close"
            @click.stop="deleteRecent(item.id)"
          />
        </div>
      </div>
    </div>

    <div
      class="history-favor"
      v-if="favorList.length"
    >
      <div class="history-title">
        <ops-icon type="veops-collect" class="history-title-icon" />
        <div class="history-title-text">{{ $t('cmdb.ciType.myCollection') }}</div>
        <div class="history-title-count">({{ favorList.length }})</div>

        <ops-icon
          type="veops-expand"
          class="history-title-expand"
          :style="{
            transform: `rotate(${isExpand ? '180deg' : '0deg'})`
          }"
          @click="isExpand = !isExpand"
        />
      </div>
      <div
        class="favor-list"
        :style="{ height: isExpand ? 'auto' : '30px' }"
      >
        <div
          v-for="(item) in favorList"
          :key="item.id"
          :class="['favor-list-item', detailCIId === item.option.CIId ? 'favor-list-item-selected' : '']"
          @click="showDetail(item.option)"
        >
          <CIIcon
            :icon="item.option.icon"
            :title="item.option.CITypeTitle"
          />
          <div class="favor-list-item-title">
            {{ item.option.title }}
          </div>
          <ops-icon
            type="veops-collected"
            class="favor-list-item-collected"
            @click.stop="deleteCollect(item.id)"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import CIIcon from '@/modules/cmdb/components/ciIcon/index.vue'

export default {
  name: 'HistoryList',
  components: {
    CIIcon
  },
  props: {
    recentList: {
      type: Array,
      default: () => []
    },
    favorList: {
      type: Array,
      default: () => []
    },
    detailCIId: {
      type: [String, Number],
      default: -1
    }
  },
  data() {
    return {
      isExpand: false,
    }
  },
  methods: {
    getRecentSearchText(option) {
      const textArray = []
      if (option.searchValue) {
        textArray.push(`${this.$t('cmdb.ciType.keyword')}: ${option.searchValue}`)
      }

      if (option?.ciTypeNames?.length) {
        textArray.push(`${this.$t('cmdb.ciType.CIType')}: ${option.ciTypeNames.join(',')}`)
      }

      if (option.expression) {
        textArray.push(`${this.$t('cmdb.ciType.conditionFilter')}: ${option.expression}`)
      }

      return textArray.join('; ')
    },

    clickRecent(data) {
      this.$emit('clickRecent', data)
    },

    deleteRecent(id) {
      this.$emit('deleteRecent', id)
    },

    deleteCollect(id) {
      this.$emit('deleteCollect', id)
    },

    showDetail(data) {
      this.$emit('showDetail', {
        id: data.CIId,
        ciTypeId: data.CITypeId
      })
    },

    clearRecent() {
      this.$emit('clearRecent')
    }
  }
}
</script>

<style lang="less" scoped>
.history-list {
  width: 100%;

  .history-title {
    display: flex;
    align-items: center;

    &-icon {
      font-size: 12px;
      color: #2F54EB;
    }

    &-text {
      font-size: 14px;
      font-weight: 400;
      color: #4E5969;
      margin-left: 4px;
    }

    &-count {
      font-size: 14px;
      font-weight: 400;
      color: #86909C;
    }

    &-clear {
      margin-left: auto;
      cursor: pointer;
    }

    &-expand {
      margin-left: auto;
      cursor: pointer;
    }
  }

  .history-recent {
    width: 100%;
    margin-top: 15px;

    .recent-list {
      margin-top: 10px;
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      column-gap: 16px;
      row-gap: 8px;

      &-item {
        flex-shrink: 0;
        padding: 4px 13px;
        display: flex;
        align-items: center;
        border-radius: 22px;
        background: rgba(255, 255, 255, 0.50);
        cursor: pointer;
        max-width: calc((100% - 16px) / 2);

        &-text {
          font-size: 12px;
          font-weight: 400;
          color: #1D2129;

          max-width: 100%;
          text-wrap: nowrap;
          text-overflow: ellipsis;
          overflow: hidden;
        }

        &-close {
          font-size: 12px;
          margin-left: 4px;
          color: #A5A9BC;
          display: none;
        }

        &:hover {
          .recent-list-item-text {
            color: #2F54EB;
          }

          .recent-list-item-close {
            display: inline-block;
          }
        }
      }
    }
  }

  .history-favor {
    width: 100%;
    margin-top: 15px;

    .favor-list {
      margin-top: 10px;
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      column-gap: 16px;
      row-gap: 8px;
      overflow: hidden;
      min-height: 30px;

      &-item {
        flex-shrink: 0;
        padding: 4px 13px;
        display: flex;
        align-items: center;
        border-radius: 22px;
        background: rgba(255, 255, 255, 0.90);
        cursor: pointer;
        max-width: calc((100% - 16px) / 2);

        &-title {
          font-size: 12px;
          font-weight: 400;
          margin-left: 4px;
          color: #1D2129;

          max-width: 100%;
          text-overflow: ellipsis;
          text-wrap: nowrap;
          overflow: hidden;
        }

        &-collected {
          font-size: 14px;
          margin-left: 4px;
          color: #FAD337;
        }

        &-selected {
          border: 1px solid #7F97FA;
          background-color: rgba(255, 255, 255, 0.90);

          .favor-list-item-title {
            color: #2F54EB;
          }
        }

        &:hover {
          .favor-list-item-title {
            color: #2F54EB;
          }
        }
      }
    }
  }
}
</style>
