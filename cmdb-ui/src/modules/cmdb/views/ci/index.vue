<template>
  <div>
    <div v-if="pageLoading" class="page-loading">
      <a-spin size="large" />
    </div>

    <div v-else-if="preferenceGroup.length === 0">
      <a-alert banner>
        <template #message>
          <span>{{ $t('cmdb.preference.tips1') }}</span>
          <router-link to="/cmdb/preference">{{ $t('cmdb.preference.tips2') }}</router-link>
          <span>{{ $t('cmdb.preference.tips3') }}</span>
        </template>
      </a-alert>
    </div>

    <SplitPane
      v-else
      appName="cmdb-ci-page"
      :min="200"
      :max="500"
      :paneLengthPixel.sync="paneLengthPixel"
      :triggerLength="18"
      calcBasedParent
    >
      <template #one>
        <div class="ci-left">
          <a-input
            :placeholder="$t('cmdb.preference.searchPlaceholder')"
            class="ci-types-left-header-input"
            @change="handleSearch"
          >
            <a-icon slot="prefix" type="search" />
          </a-input>

          <div class="ci-left-list">
            <div
              v-for="(group) in filterPreferenceGroup"
              :key="group.key"
              class="ci-left-group"
            >
              <div class="ci-left-group-name">{{ group.name }}</div>
              <div
                v-for="(type) in group.children"
                :key="type.key"
                :class="['ci-left-item', currentTypeId === type.id ? 'ci-left-item_active' : '']"
                @click="updateTypeId(type.id)"
              >
                <CIIcon :icon="type.icon" :title="type.alias || type.name" :size="16" />
                <span class="ci-left-item-name">{{ type.alias || type.name }}</span>
                <a-dropdown>
                  <a class="ci-left-item-more">
                    <ops-icon type="veops-more" />
                  </a>
                  <a-menu slot="overlay">
                    <a-menu-item @click="handlePerm(type)">
                      <a-icon type="user-add" />
                      {{ $t('grant') }}
                    </a-menu-item>
                    <a-menu-item
                      v-if="!autoSub.enabled"
                      @click="cancelSub(type)"
                    >
                      <a-icon type="star" />
                      {{ $t('cmdb.preference.cancelSub') }}
                    </a-menu-item>
                  </a-menu>
                </a-dropdown>
              </div>
            </div>
          </div>
        </div>

        <CMDBGrant ref="cmdbGrantCIType" resourceType="CIType" app_id="cmdb" />
      </template>
      <template #two>
        <InstanceList
          v-if="currentTypeId"
          :key="Number(currentTypeId)"
          :typeId="Number(currentTypeId)"
          :CIType="currentCIType"
          :autoSub="autoSub"
          @unSubscribe="getPreference"
        />
      </template>
    </SplitPane>
  </div>
</template>

<script>
import _ from 'lodash'
import { getPreference, subscribeCIType, subscribeTreeView } from '@/modules/cmdb/api/preference'
import { roleHasPermissionToGrant } from '@/modules/acl/api/permission'
import { searchResourceType } from '@/modules/acl/api/resource'
import { getAutoSubscription } from '@/modules/cmdb/api/preference.js'

import SplitPane from '@/components/SplitPane'
import CIIcon from '@/modules/cmdb/components/ciIcon'
import InstanceList from './instanceList.vue'
import CMDBGrant from '@/modules/cmdb/components/cmdbGrant'

export default {
  name: 'CIPage',
  components: {
    SplitPane,
    CIIcon,
    InstanceList,
    CMDBGrant
  },
  data() {
    return {
      paneLengthPixel: 205,
      searchValue: '',
      preferenceGroup: [],
      currentTypeId: Number(this.$route?.params?.typeId || localStorage.getItem('ops_ci_typeid') || ''),
      resource_type: {},
      autoSub: {},
      pageLoading: false
    }
  },
  computed: {
    currentCIType() {
      let CIType = {}
      this.preferenceGroup.some((group) => {
        const type = group.children.find((item) => item.id === this.currentTypeId)
        if (type) {
          CIType = type
        }

        return type
      })

      return CIType
    },
    filterPreferenceGroup() {
      if (!this?.preferenceGroup?.length) {
        return []
      }

      if (!this.searchValue) {
        return this.preferenceGroup
      }

      const preferenceGroup = _.cloneDeep(this.preferenceGroup)
      preferenceGroup.forEach((group) => {
        if (group?.name?.indexOf?.(this.searchValue) >= 0) {
          return
        }

        group.children = group?.children?.filter?.((item) => item?.alias?.indexOf?.(this.searchValue) >= 0 || item?.name?.indexOf?.(this.searchValue) >= 0) || []
      })
      return preferenceGroup.filter((group) => group?.children?.length)
    },
  },
  provide() {
    return {
      resource_type: () => {
        return this.resource_type
      },
    }
  },
  created() {
    this.pageLoading = true
    Promise.all([
      this.getPreference(),
      this.getResourceType(),
      this.getAutoSubscription()
    ]).then(() => {
      this.pageLoading = false
    })
  },
  methods: {
    async getPreference() {
      const res = await getPreference()
      const groupTypes = (res?.group_types || []).filter((group) => group?.ci_types?.length)
      const preferenceGroup = groupTypes.map((group) => {
        const children = group.ci_types.map((type) => {
          return {
            ...type,
            key: `ci_type_${type.id}`
          }
        })

        return {
          name: group.name,
          id: group.id,
          key: `group_${group.id}`,
          children
        }
      })

      this.preferenceGroup = preferenceGroup

      if (!preferenceGroup.length) {
        this.currentTypeId = ''
        return
      }

      if (
        !this.currentTypeId ||
        !preferenceGroup.some((group) => group.children.some((item) => item.id === this.currentTypeId))
      ) {
        this.updateTypeId(preferenceGroup[0].children[0].id)
      }
    },

    async getResourceType() {
      await searchResourceType({ page_size: 9999, app_id: 'cmdb' }).then(res => {
        this.resource_type = { groups: res.groups, id2perms: res.id2perms }
      })
    },

    async getAutoSubscription() {
      const res = await getAutoSubscription()
      this.autoSub = res || {}
    },

    updateTypeId(id) {
      if (id !== this.currentTypeId) {
        this.currentTypeId = id
        localStorage.setItem('ops_ci_typeid', id)
      }
    },

    handleSearch(e) {
      this.searchValue = e.target.value
    },

    handlePerm(type) {
      roleHasPermissionToGrant({
        app_id: 'cmdb',
        resource_type_name: 'CIType',
        perm: 'grant',
        resource_name: type.name,
      }).then(res => {
        if (res.result) {
          this.$refs.cmdbGrantCIType.open({ name: type.name, cmdbGrantType: 'ci', CITypeId: type.id })
        } else {
          this.$message.error(this.$t('noPermission'))
        }
      })
    },

    cancelSub(type) {
      this.$confirm({
        title: this.$t('warning'),
        content: this.$t('cmdb.preference.confirmcancelSub2', { name: type.alias || type.name }),
        onOk: () => {
          const unsubCIType = subscribeCIType(type.id, '')
          const unsubTree = subscribeTreeView(type.id, '')
          Promise.all([unsubCIType, unsubTree]).then(() => {
            this.$message.success(this.$t('cmdb.preference.cancelSubSuccess'))
            this.getPreference()
          })
        },
      })
    },
  }
}
</script>

<style lang="less" scoped>
.page-loading {
  text-align: center;
  padding-top: 150px;
}

.ci-types-left-header-input {
  margin-bottom: 12px;

  /deep/ input {
    background-color: #fff;
    border-radius: 6px;
    border: 1px solid #e8eaed;
    transition: all 0.2s ease;

    &:hover {
      border-color: #c3cdd7;
    }

    &:focus {
      border-color: @primary-color;
      box-shadow: 0 0 0 2px fade(@primary-color, 10%);
    }
  }

  /deep/ .ant-input-prefix {
    color: @text-color_3;
  }
}

.ci-left {
  height: calc(100vh - 90px);
  width: 100%;
  background-color: #f7f8fa;
  border-right: 1px solid #e8eaed;
  padding: 0px 8px 12px;

  &-list {
    width: 100%;
    height: calc(100% - 40px);
    overflow: hidden;

    &:hover {
      overflow-y: auto;
    }
  }

  &-group {
    width: 100%;

    &:not(:last-child) {
      margin-bottom: 12px;
    }

    &-name {
      margin-bottom: 8px;
      font-weight: 600;
      font-size: 13px;
      color: #666;
      padding: 8px 12px;
    }
  }

  &-item {
    width: 100%;
    display: flex;
    align-items: center;
    padding: 6px 12px;
    margin: 0 4px 6px 4px;
    cursor: pointer;
    border-radius: 6px;
    height: 36px;
    position: relative;
    transition: all 0.2s ease;

    &::before {
      content: "";
      position: absolute;
      left: 0;
      top: 0;
      bottom: 0;
      width: 3px;
      background: @primary-color;
      border-radius: 0 2px 2px 0;
      opacity: 0;
      transition: opacity 0.2s ease;
    }

    .ci-icon {
      width: 24px;
      height: 24px;
      display: flex;
      align-items: center;
      justify-content: center;
      background: #fff;
      border: 1px solid #e8eaed;
      border-radius: 6px;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
      flex-shrink: 0;
      transition: transform 0.2s ease;
    }

    &-name {
      margin-left: 8px;
      margin-right: 8px;
      text-wrap: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      font-size: 14px;
      color: @text-color_1;
      transition: color 0.2s ease;
      flex: 1;
    }

    &-more {
      margin-left: auto;
      display: none;
      flex-shrink: 0;
    }

    &_active {
      background-color: @primary-color_6;
      box-shadow: 0 1px 3px fade(@primary-color, 10%);

      &::before {
        opacity: 1;
      }

      .ci-left-item-name {
        color: @primary-color;
        font-weight: 600;
      }

      .ci-icon {
        box-shadow: 0 2px 4px fade(@primary-color, 20%);
      }
    }

    &:hover {
      background-color: @primary-color_7;
      transform: translateX(2px);

      .ci-icon {
        transform: scale(1.05);
      }

      .ci-left-item-more {
        display: block;
      }
    }
  }
}
</style>
