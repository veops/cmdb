<template>
  <div class="cmdb-preference" :style="{ height: `${windowHeight - 40}px` }">
    <div class="cmdb-preference-left">
      <div class="cmdb-preference-left-card">
        <span class="cmdb-preference-left-card-title">{{ $t('cmdb.preference.mySub') }}</span>
        <span
          class="cmdb-preference-left-card-content"
        ><ops-icon type="cmdb-ci" :style="{ marginRight: '5px' }" />{{ $t('cmdb.menu.ciTable') }}:
          <a-badge
            showZero
            :count="self.instance.length"
            :overflow-count="99"
            :number-style="{
              backgroundColor: 'inherit',
              boxShadow: 'none',
              height: '23px',
              fontSize: '14px',
            }"
          /></span
        >
        <span
          class="cmdb-preference-left-card-content"
        ><ops-icon type="cmdb-tree" :style="{ marginRight: '5px' }" />{{ $t('cmdb.menu.ciTree') }}:
          <a-badge
            showZero
            :count="self.tree.length"
            :overflow-count="99"
            :number-style="{
              backgroundColor: 'inherit',
              boxShadow: 'none',
              height: '23px',
              fontSize: '14px',
            }"
          /></span
        >
      </div>
      <div class="cmdb-preference-group" v-for="(group, index) in myPreferences" :key="group.name">
        <div class="cmdb-preference-group-title">
          <span> <ops-icon :style="{ marginRight: '10px' }" :type="group.icon" />{{ group.name }} </span>
        </div>
        <div class="cmdb-preference-group-content" v-for="ciType in group.ci_types" :key="ciType.id">
          <div
            :class="{
              'cmdb-preference-avatar': true,
              'cmdb-preference-avatar-noicon': !ciType.icon,
              'cmdb-preference-avatar-noicon-is_subscribed': !ciType.icon,
            }"
            :style="{ width: '30px', height: '30px', marginRight: '10px' }"
          >
            <template v-if="ciType.icon">
              <img
                v-if="ciType.icon.split('$$')[2]"
                :src="`/api/common-setting/v1/file/${ciType.icon.split('$$')[3]}`"
                :style="{ maxHeight: '30px', maxWidth: '30px' }"
              />
              <ops-icon
                v-else
                :style="{
                  color: ciType.icon.split('$$')[1],
                  fontSize: '14px',
                }"
                :type="ciType.icon.split('$$')[0]"
              />
            </template>
            <span v-else :style="{ fontSize: '20px' }">{{ ciType.name[0].toUpperCase() }}</span>
          </div>
          <span class="cmdb-preference-group-content-title">{{ ciType.alias || ciType.name }}</span>
          <span class="cmdb-preference-group-content-action">
            <a-tooltip :title="$t('cmdb.preference.cancelSub')">
              <span
                @click="unsubscribe(ciType, group.type)"
              ><ops-icon type="cmdb-preference-cancel-subscribe" />
              </span>
            </a-tooltip>
            <a-divider type="vertical" :style="{ margin: '0 3px' }" />
            <a-tooltip :title="$t('cmdb.preference.editSub')">
              <span
                @click="openSubscribeSetting(ciType, `${index + 1}`)"
              ><ops-icon
                type="cmdb-preference-subscribe"
              /></span>
            </a-tooltip>
          </span>
        </div>
      </div>
    </div>
    <div class="cmdb-preference-right">
      <div v-for="group in citypeData" :key="group.id">
        <p @click="changeGroupExpand(group)" :style="{ display: 'inline-block', cursor: 'pointer' }">
          <a-icon :type="expandKeys.includes(group.id) ? 'caret-down' : 'caret-right'" />{{ group.name }}({{
            group.ci_types ? group.ci_types.length : 0
          }})
        </p>
        <CollapseTransition v-show="expandKeys.includes(group.id)" :key="group.id">
          <div class="cmdb-preference-content">
            <div class="cmdb-preference-type" v-for="item in group.ci_types" :key="item.id">
              <div class="cmdb-preference-header">
                <div
                  :class="{
                    'cmdb-preference-avatar': true,
                    'cmdb-preference-avatar-noicon': !item.icon,
                    'cmdb-preference-avatar-noicon-is_subscribed': !item.icon && item.is_subscribed,
                  }"
                >
                  <template v-if="item.icon">
                    <img
                      v-if="item.icon.split('$$')[2]"
                      :src="`/api/common-setting/v1/file/${item.icon.split('$$')[3]}`"
                      :style="{ maxHeight: '30px', maxWidth: '30px' }"
                    />
                    <ops-icon
                      v-else
                      :style="{
                        color: item.icon.split('$$')[1],
                        fontSize: '14px',
                      }"
                      :type="item.icon.split('$$')[0]"
                    />
                  </template>
                  <span v-else>{{ item.name[0].toUpperCase() }}</span>
                </div>
                <span class="cmdb-preference-title" :title="item.alias || item.name">
                  {{ item.alias || item.name }}</span
                >
              </div>
              <div class="cmdb-preference-colleague">
                <template v-if="type_id2users[item.id] && type_id2users[item.id].length">
                  <span
                  >{{ type_id2users[item.id].length > 99 ? '99+' : type_id2users[item.id].length
                  }}{{ $t('cmdb.preference.peopleSub') }}</span
                  >
                  <span class="cmdb-preference-colleague-name">
                    <span v-for="uid in type_id2users[item.id].slice(0, 4)" :key="uid">
                      {{ getNameByUid(uid) }}
                    </span>
                    <span class="cmdb-preference-colleague-ellipsis" v-if="type_id2users[item.id].length > 4">...</span>
                  </span>
                </template>
                <span v-else :style="{ marginLeft: 'auto' }">{{ $t('cmdb.preference.noSub') }}</span>
              </div>
              <div class="cmdb-preference-progress">
                <div class="cmdb-preference-progress-info">
                  <span>{{ $t('cmdb.menu.ad') }}</span>
                  <span>{{ item.integrity }}%</span>
                </div>
                <div class="cmdb-preference-progress-gray">
                  <div class="cmdb-preference-progress-colors" :style="{ width: `${item.integrity}%` }"></div>
                </div>
              </div>
              <a-divider :style="{ margin: '10px 0 3px 0' }" />
              <div class="cmdb-preference-footor-subscribed" v-if="item.is_subscribed">
                <span><a-icon type="clock-circle" :style="{ marginRight: '3px' }" />{{ getsubscribedDays(item) }}</span>
                <span>
                  <a-tooltip :title="$t('cmdb.preference.cancelSub')">
                    <span @click="unsubscribe(item)"><ops-icon type="cmdb-preference-cancel-subscribe" /> </span>
                  </a-tooltip>
                  <a-divider type="vertical" :style="{ margin: '0 3px' }" />
                  <a-tooltip :title="$t('cmdb.preference.editSub')">
                    <span @click="openSubscribeSetting(item)"><ops-icon type="cmdb-preference-subscribe"/></span>
                  </a-tooltip>
                </span>
              </div>
              <div v-else class="cmdb-preference-footor-unsubscribed">
                <span
                  @click="openSubscribeSetting(item)"
                ><ops-icon :style="{ marginRight: '3px' }" type="cmdb-preference-subscribe" />{{
                  $t('cmdb.preference.sub')
                }}</span
                >
              </div>
            </div>
            <i></i><i></i><i></i><i></i><i></i>
          </div>
        </CollapseTransition>
      </div>
    </div>
    <SubscribeSetting
      ref="subscribeSetting"
      @reload="
        () => {
          resetRoute()
        }
      "
    />
  </div>
</template>

<script>
import router, { resetRouter } from '@/router'
import store from '@/store'
import { mapState } from 'vuex'
import moment from 'moment'
import { getCITypeGroups } from '../../api/ciTypeGroup'
import { getPreference, getPreference2, subscribeCIType, subscribeTreeView } from '@/modules/cmdb/api/preference'
import CollapseTransition from '@/components/CollapseTransition'
import SubscribeSetting from '../../components/subscribeSetting/subscribeSetting'
import { getCIAdcStatistics } from '../../api/ci'

export default {
  name: 'Preference',
  components: { CollapseTransition, SubscribeSetting },
  data() {
    return {
      citypeData: [],
      expandKeys: [],
      self: {
        instance: [],
        tree: [],
      },
      type_id2users: {},
      myPreferences: [],
    }
  },
  computed: {
    ...mapState({
      windowHeight: (state) => state.windowHeight,
      allUsers: (state) => state.user.allUsers,
    }),
  },
  mounted() {
    this.getCITypes(true)
  },
  methods: {
    async getCITypes(isInit = false) {
      const [ciTypeGroup, pref, pref2, statistics] = await Promise.all([
        getCITypeGroups({ need_other: true }),
        getPreference(true, true),
        getPreference2(true, true),
        getCIAdcStatistics(),
      ])
      ciTypeGroup.forEach((group) => {
        if (group.ci_types && group.ci_types.length) {
          group.ci_types.forEach((type) => {
            const idx = pref.findIndex((p) => p.id === type.id)
            if (idx > -1) {
              type.is_subscribed = true
            }
            const type_statistic = statistics[type.id]
            type.integrity = type_statistic
              ? Math.round((type_statistic.auto_discovery * 100) / type_statistic.total)
              : 0
          })
        }
        if (!group.id) {
          group.id = -1
          group.name = this.$t('other')
        }
      })
      this.citypeData = ciTypeGroup
      const { self, type_id2users } = pref2
      this.self = self
      this.type_id2users = type_id2users
      const _myPreferences = [
        {
          name: this.$t('cmdb.menu.ciTable'),
          ci_types: self.instance.map((item) => {
            const _find = pref.find((ci) => ci.id === item)
            return _find
          }),
          icon: 'cmdb-ci',
          type: 'ci',
        },
        {
          name: this.$t('cmdb.menu.ciTree'),
          ci_types: self.tree.map((item) => {
            const _find = pref.find((ci) => ci.id === item)
            return _find
          }),
          icon: 'cmdb-tree',
          type: 'tree',
        },
      ]
      this.myPreferences = _myPreferences
      if (isInit) {
        setTimeout(() => {
          this.expandKeys = ciTypeGroup.map((item) => item.id)
        }, 300)
      }
    },
    getNameByUid(uid) {
      const _find = this.allUsers.find((item) => item.uid === uid)
      return _find?.username[0].toUpperCase() || 'A'
    },
    getsubscribedDays(item) {
      const subscribedTime = this.self.type_id2subs_time[item.id]
      moment.duration(moment().diff(moment(subscribedTime)))
      const day = moment().diff(moment(subscribedTime), 'day')
      if (day > 0 && day < 1) {
        return `${moment().diff(moment(subscribedTime), 'hour')}` + this.$t('cmdb.preference.hoursAgo')
      } else if (day >= 1 && day <= 31) {
        return `${day} ` + this.$t('cmdb.preference.daysAgo')
      } else if (day > 31 && day < 365) {
        return `${moment().diff(moment(subscribedTime), 'month')}` + this.$t('cmdb.preference.monthsAgo')
      } else if (day >= 365) {
        return `${moment().diff(moment(subscribedTime), 'year')}` + this.$t('cmdb.preference.yearsAgo')
      }
      return this.$t('cmdb.preference.just')
    },
    unsubscribe(ciType, type = 'all') {
      const that = this
      this.$confirm({
        title: that.$t('warning'),
        content:
          that.$t('cmdb.preference.confirmcancelSub') +
          ` ${ciType.alias || ciType.name} ${
            type !== 'all'
              ? that.$t('cmdb.preference.of') +
                `${type === 'ci' ? this.$t('cmdb.menu.ciTable') : that.$t('cmdb.menu.ciTree')}`
              : ''
          } ？`,
        onOk() {
          const promises = []
          if (type === 'all' || type === 'ci') {
            const unsubCIType = subscribeCIType(ciType.id, '')
            promises.push(unsubCIType)
          }
          if (type === 'all' || type === 'tree') {
            const unsubTree = subscribeTreeView(ciType.id, '')
            promises.push(unsubTree)
          }

          Promise.all(promises).then(() => {
            if (type === 'all' || type === 'ci') {
              const lastTypeId = window.localStorage.getItem('ops_ci_typeid') || undefined
              if (Number(ciType.id) === Number(lastTypeId)) {
                localStorage.setItem('ops_ci_typeid', '')
              }
            }
            that.$message.success(that.$t('cmdb.preference.cancelSubSuccess'))
            that.resetRoute()
          })
        },
      })
    },
    resetRoute() {
      resetRouter()
      const roles = store.getters.roles
      store.dispatch('GenerateRoutes', { roles }, { root: true }).then(() => {
        router.addRoutes(store.getters.appRoutes)
        this.getCITypes()
      })
    },
    openSubscribeSetting(ciType, activeKey = '1') {
      this.$refs.subscribeSetting.open({ ...ciType, type_id: ciType.id }, activeKey)
    },
    changeGroupExpand(group) {
      const _idx = this.expandKeys.findIndex((expand) => expand === group.id)
      if (_idx > -1) {
        this.expandKeys.splice(_idx, 1)
      } else {
        this.expandKeys.push(group.id)
      }
    },
  },
}
</script>

<style lang="less" scoped>
@import '~@/style/static.less';
.cmdb-preference {
  margin: -24px;
  overflow: auto;
  background: url('../../assets/preference_background.png');
  position: relative;
  display: flex;
  flex-direction: row;
  &::before {
    content: '';
    position: absolute;
    box-shadow: 0px 1px 4px rgba(0, 21, 41, 0.5);
    width: 100%;
    left: 0;
    height: 1px;
    top: 0;
  }
  .cmdb-preference-left {
    width: 300px;
    height: 100%;
    padding: 12px 18px;
    .cmdb-preference-left-card {
      background: url('../../assets/preference_card.png');
      background-repeat: no-repeat;
      background-position-x: center;
      background-position-y: center;
      height: 172px;
      background-size: 90%;
      color: #fff;
      position: relative;
      .cmdb-preference-left-card-title {
        font-weight: 600;
        position: absolute;
        top: 32px;
        left: 36px;
      }
      .cmdb-preference-left-card-content {
        position: absolute;
        left: 36px;
      }
      .cmdb-preference-left-card-content:nth-child(2) {
        top: 65px;
      }
      .cmdb-preference-left-card-content:nth-child(3) {
        top: 95px;
      }
    }
    .cmdb-preference-group:nth-child(2) {
      margin-bottom: 20px;
    }
    .cmdb-preference-group {
      .cmdb-preference-group-title {
        text-align: center;
        margin-bottom: 5px;
        > span {
          display: inline-block;
          color: #fff;
          background: linear-gradient(90deg, #305bec, #78cfff);
          border-radius: 16px;
          font-weight: 600;
          padding: 6px 12px;
        }
      }
      .cmdb-preference-group-content {
        color: rgba(0, 0, 0, 0.75);
        font-weight: 400;
        display: flex;
        align-items: center;
        height: 45px;
        padding: 0 8px;
        cursor: default;
        justify-content: flex-start;
        &:hover {
          background: #ffffff;
          box-shadow: 0px 2px 8px rgba(149, 160, 208, 0.25);
          border-radius: 8px;
          .cmdb-preference-group-content-action {
            display: inline;
            white-space: nowrap;
            margin-left: auto;
          }
        }
        .cmdb-preference-group-content-title {
          flex: 1;
        }
        .cmdb-preference-group-content-action {
          margin-left: auto;
          font-size: 12px;
          color: #custom_colors[color_1];
          cursor: pointer;
          display: none;
        }
      }
    }
  }
  .cmdb-preference-right {
    flex: 1;
    height: 100%;
    padding-top: 18px;
    .cmdb-preference-content {
      display: flex;
      flex-direction: row;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      > i {
        width: 195px;
        margin: 0 20px 0 0;
      }
      .cmdb-preference-type {
        display: inline-block;
        width: 195px;
        height: 155px;
        border-radius: 8px;
        background-color: #fff;
        box-shadow: 0px 2px 8px rgba(149, 160, 208, 0.25);
        margin: 0 20px 20px 0;
        padding: 8px;
        &:hover {
          box-shadow: 4px 25px 30px rgba(50, 89, 134, 0.25);
          transform: scale(1.1);
        }
        .cmdb-preference-header {
          display: flex;
          align-items: center;
          justify-content: flex-start;
          .cmdb-preference-title {
            color: rgba(0, 0, 0, 0.75);
            font-weight: 500;
            margin-left: 12px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            flex: 1;
          }
        }
        .cmdb-preference-colleague {
          color: rgba(0, 0, 0, 0.45);
          font-size: 12px;
          margin-top: 10px;
          height: 18px;
          display: flex;
          flex-direction: row;
          align-items: center;
          justify-content: space-between;
          .cmdb-preference-colleague-name > span:not(.cmdb-preference-colleague-ellipsis) {
            display: inline-block;
            color: rgba(0, 0, 0, 0.5);
            height: 14px;
            width: 14px;
            background-color: #f0f5ff;
            border-radius: 50%;
            font-size: 12px;
            line-height: 14px;
            text-align: center;
            margin-right: 2px;
          }
        }
        .cmdb-preference-progress {
          font-size: 12px;
          color: rgba(0, 0, 0, 0.76);
          margin-top: 10px;
          .cmdb-preference-progress-info {
            display: flex;
            justify-content: space-between;
          }
          .cmdb-preference-progress-gray {
            height: 5px;
            border-radius: 5px;
            background-color: #d9d9d9;
            margin-top: 5px;
            width: 100%;
            position: relative;
            .cmdb-preference-progress-colors {
              height: 5px;
              position: absolute;
              top: 0;
              left: 0;
              border-radius: 5px;
              background: linear-gradient(90deg, #305bec, #78cfff);
            }
          }
        }
        .cmdb-preference-footor-unsubscribed {
          text-align: center;
          > span {
            color: #custom_colors[color_1];
            cursor: pointer;
            font-size: 12px;
          }
        }
        .cmdb-preference-footor-subscribed {
          display: flex;
          justify-content: space-between;
          font-size: 12px;
          > span:first-child {
            color: rgba(0, 0, 0, 0.45);
          }
          > span:nth-child(2) {
            color: #custom_colors[color_1];
            cursor: pointer;
          }
        }
      }
    }
  }

  .cmdb-preference-avatar {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    box-shadow: 0px 4px 4px rgba(129, 140, 186, 0.25);
    border-radius: 5px;
  }
  .cmdb-preference-avatar-noicon {
    background-color: #7f97fa;
    > span {
      font-size: 24px;
      color: #fff;
    }
  }
  .cmdb-preference-avatar-noicon-is_subscribed {
    background-color: #47a964;
  }
}
</style>
