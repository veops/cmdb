<template>
  <div class="counter-wrap">
    <div
      v-for="(group, groupIndex) in counterData"
      :key="groupIndex"
      class="counter-group"
    >
      <div
        v-for="(item, index) in group"
        :key="index"
        class="counter-item"
      >
        <div class="counter-item-header">
          <ops-icon class="counter-item-icon" :type="item.icon" />
          <span
            class="counter-item-title"
            :title="$t(item.title)"
          >
            {{ $t(item.title) }}
          </span>
        </div>
        <div>
          <span class="counter-item-number">{{ item.count }}</span>
          <template v-if="item.percent !== undefined">
            <span
              v-if="item.percent !== -1"
              :class="['counter-item-percent', 'counter-item-percent-' + (item.percentStatus ? 'up' : 'down')]"
            >
              <ops-icon class="counter-item-percent-icon" type="cmdb-arrow" />
              <span
                class="counter-item-percent-text"
              >
                {{ item.percent }}%
              </span>
            </span>
            <span
              v-else
              class="counter-item-percent-null"
            >
              -
            </span>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import _ from 'lodash'
import { getAdcCounter } from '@/modules/cmdb/api/discovery'

export default {
  name: 'AdcCounter',
  props: {
    typeId: {
      type: Number,
      default: 0,
    }
  },
  data() {
    return {
      counterDataTemplate: [
        [
          {
            title: 'cmdb.ad.ruleCount',
            icon: 'cmdb-rule',
            type: 'ruleCount',
            count: 0,
          },
          {
            title: 'cmdb.ad.execMachine',
            icon: 'cmdb-executing_machine',
            type: 'execTargetCount',
            count: 0,
          },
        ],
        [
          {
            title: 'cmdb.ad.resource',
            icon: 'cmdb-resource',
            type: 'resource',
            count: 0,
          },
          {
            title: 'cmdb.ad.autoInventory',
            icon: 'cmdb-automatic_inventory',
            type: 'autoInventory',
            count: 0,
          },
        ],
        [
          {
            title: 'cmdb.ad.newThisWeek',
            icon: 'cmdb-week_additions',
            type: 'rule_count',
            count: 0,
            percentStatus: true,
            percent: '',
          },
          {
            title: 'cmdb.ad.newThisMonth',
            icon: 'cmdb-month_additions',
            type: 'rule_count',
            count: 0,
            percentStatus: true,
            percent: '',
          }
        ]
      ],
      counterData: [],
    }
  },
  watch: {
    typeId: {
      immediate: true,
      handler(id) {
        if (id) {
          this.queryAdcCounter(id)
        }
      }
    }
  },
  methods: {
    async queryAdcCounter(id) {
      const res = await getAdcCounter({
        type_id: id
      })
      console.log('getAdcCounter res', res)
      const _counterData = _.cloneDeep(this.counterDataTemplate)

      _counterData[0][0]['count'] = res?.rule_count ?? 0
      _counterData[0][1]['count'] = res?.exec_target_count ?? 0

      _counterData[1][0]['count'] = res?.instance_count ?? 0
      _counterData[1][1]['count'] = res?.accept_count ?? 0

      const newWeekCount = Math.abs(res.this_week_count - res.last_week_count)
      const newWeekPrecent = res.last_week_count ? Number((newWeekCount / res.last_week_count).toFixed(2)) * 100 : -1
      _counterData[2][0]['count'] = res.this_week_count || 0
      _counterData[2][0]['percent'] = newWeekPrecent
      _counterData[2][0]['percentStatus'] = res.this_week_count >= res.last_week_count

      const newMonthCount = Math.abs(res.this_month_count - res.last_month_count)
      const newMonthPrecent = res.last_month_count ? Number((newMonthCount / res.last_month_count).toFixed(2)) * 100 : -1
      _counterData[2][1]['count'] = res.this_month_count || 0
      _counterData[2][1]['percent'] = newMonthPrecent
      _counterData[2][1]['percentStatus'] = res.this_month_count >= res.last_month_count

      this.counterData = _counterData
    }
  }
}
</script>

<style lang="less" scoped>
.counter-wrap {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;

  .counter-group {
    display: flex;
    align-items: center;
    height: 82px;
    border: solid 1px @border-color-base;
    flex-grow: 0;
    width: calc((100% - 30px) / 3);

    .counter-item {
      padding: 16px 18px;
      flex-grow: 0;
      width: 50%;

      &-header {
        width: 100%;
        display: flex;
        align-items: center;
      }

      &-icon {
        font-size: 14px;
      }

      &-title {
        font-size: 14px;
        color: @text-color_2;
        margin-left: 4px;

        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        flex-grow: 0;
      }

      &-number {
        color: @primary-color;
        font-size: 22px;
        font-weight: 700;
      }

      &-percent {
        margin-left: 5px;

        &-icon {
          font-size: 12px;
        }

        &-text {
          font-size: 10px;
          font-weight: 400;
        }

        &-up {
          color: #00B42A;
        }

        &-down {
          color: #FD4C6A;

          .counter-item-percent-icon {
            transform: rotate(180deg);
          }
        }
      }

      &-percent-null {
        padding: 0 10px;
      }
    }
  }
}
</style>
