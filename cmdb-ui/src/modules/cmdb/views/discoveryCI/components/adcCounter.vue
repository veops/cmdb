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
  gap: 16px;
  margin-bottom: 16px;

  .counter-group {
    display: flex;
    align-items: stretch;
    height: 90px;
    border: 1px solid #e8eaed;
    border-radius: 8px;
    flex-grow: 0;
    width: calc((100% - 32px) / 3);
    background: #fff;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    transition: all 0.3s ease;
    overflow: hidden;

    &:hover {
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
      transform: translateY(-2px);
    }

    .counter-item {
      padding: 16px 20px;
      flex-grow: 0;
      width: 50%;
      position: relative;

      &:not(:last-child)::after {
        content: '';
        position: absolute;
        right: 0;
        top: 20px;
        bottom: 20px;
        width: 1px;
        background: #e8eaed;
      }

      &-header {
        width: 100%;
        display: flex;
        align-items: center;
        margin-bottom: 8px;
      }

      &-icon {
        font-size: 16px;
        color: @primary-color;
      }

      &-title {
        font-size: 13px;
        color: @text-color_2;
        margin-left: 6px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        flex-grow: 0;
      }

      &-number {
        color: @text-color_1;
        font-size: 24px;
        font-weight: 600;
      }

      &-percent {
        margin-left: 8px;
        display: inline-flex;
        align-items: center;
        gap: 2px;

        &-icon {
          font-size: 12px;
        }

        &-text {
          font-size: 12px;
          font-weight: 500;
        }

        &-up {
          color: #00B42A;
        }

        &-down {
          color: #F53F3F;

          .counter-item-percent-icon {
            transform: rotate(180deg);
          }
        }
      }

      &-percent-null {
        padding: 0 8px;
        color: @text-color_4;
      }
    }
  }
}
</style>
