<template>
  <div class="builtin">
    <div class="builtin-tab">
      <div
        v-for="(item) in tabList"
        :key="item.key"
        :class="['builtin-tab-item', activeKey === item.key ? 'builtin-tab-item_active' : '']"
        @click="clickTab(item.key)"
      >
        <ops-icon :type="item.icon" class="builtin-tab-item-icon" />
        <span class="builtin-tab-item-title">{{ $t(item.title) }}</span>
      </div>
    </div>

    <div
      v-if="activeKey === BUILT_IN_TYPE.DEPARTMENT"
      class="builtin-department"
    >
      <a-icon class="builtin-department-icon" type="info-circle" />
      <span class="builtin-department-tip">{{ $t('cmdb.ciType.departmentTip') }}</span>
    </div>

    <a-form
      :form="form"
      v-show="activeKey === BUILT_IN_TYPE.USER"
      class="builtin-user"
    >
      <a-form-item
        :label="$t('cmdb.ciType.filterUsers')"
        :label-col="formLayout.labelCol"
        :wrapper-col="formLayout.wrapperCol"
      >
        <UserFilterComp
          ref="userFilterRef"
        />
      </a-form-item>

      <a-form-item
        :label="$t('cmdb.ciType.departmentCascadeDisplay')"
        v-if="activeKey === BUILT_IN_TYPE.USER"
        :label-col="formLayout.labelCol"
        :wrapper-col="formLayout.wrapperCol"
      >
        <a-switch
          v-decorator="['cascade_display', { rules: [{ required: false }], valuePropName: 'checked', initialValue: false }]"
        ></a-switch>
      </a-form-item>

      <a-form-item
        v-if="activeKey === BUILT_IN_TYPE.USER"
        :label="$t('cmdb.ciType.displayValue')"
        :label-col="formLayout.labelCol"
        :wrapper-col="formLayout.wrapperCol"
      >
        <a-select
          class="builtin-select"
          v-decorator="['display_value', { rules: [{ required: true, message: $t('cmdb.ciType.displayValueSelectTip') }], initialValue: 'nickname' }]"
          showSearch
          optionFilterProp="title"
          :placeholder="$t('cmdb.ciType.displayValueSelectTip')"
        >
          <a-select-option
            v-for="(item) in DISPLAY_VALUE_SELECT"
            :value="item.value"
            :key="item.value"
            :title="$t(item.label)"
          >
            {{ $t(item.label) }}
          </a-select-option>
        </a-select>
      </a-form-item>
    </a-form>

    <a-form
      :form="form"
      v-if="activeKey === BUILT_IN_TYPE.USER_GROUP"
      class="builtin-usergroup"
    >
      <a-form-item
        :label="$t('cmdb.ciType.userGroup')"
        :label-col="formLayout.labelCol"
        :wrapper-col="formLayout.wrapperCol"
      >
        <a-select
          class="builtin-select"
          v-decorator="['user_group_key', { rules: [{ required: true, message: $t('cmdb.ciType.userGroupSelectTip') }] }]"
          showSearch
          optionFilterProp="title"
          :placeholder="$t('cmdb.ciType.userGroupSelectTip')"
        >
          <a-select-option
            v-for="(item) in userGroupList"
            :value="item.group_id"
            :key="item.group_id"
            :title="item.group_name"
          >
            {{ item.group_name }}
          </a-select-option>
        </a-select>
      </a-form-item>

      <a-form-item
        :label-col="formLayout.labelCol"
        :wrapper-col="formLayout.wrapperCol"
        :label="$t('cmdb.ciType.displayValue')"
      >
        <a-select
          class="builtin-select"
          v-decorator="['display_value', { rules: [{ required: true, message: $t('cmdb.ciType.displayValueSelectTip') }], initialValue: 'nickname' }]"
          showSearch
          optionFilterProp="title"
          :placeholder="$t('cmdb.ciType.displayValueSelectTip')"
        >
          <a-select-option
            v-for="(item) in DISPLAY_VALUE_SELECT"
            :value="item.value"
            :key="item.value"
            :title="$t(item.label)"
          >
            {{ $t(item.label) }}
          </a-select-option>
        </a-select>
      </a-form-item>
    </a-form>
  </div>
</template>

<script>
import { BUILT_IN_TYPE, DISPLAY_VALUE_SELECT } from './constants.js'
import UserFilterComp from './userFilterComp/index.vue'

export default {
  name: 'PreValueBuiltIn',
  components: { UserFilterComp },
  data() {
    return {
      BUILT_IN_TYPE,
      DISPLAY_VALUE_SELECT,
      activeKey: BUILT_IN_TYPE.DEPARTMENT,
      tabList: [
        {
          key: BUILT_IN_TYPE.DEPARTMENT,
          title: 'cmdb.ciType.department',
          icon: 'veops-department'
        },
        {
          key: BUILT_IN_TYPE.USER,
          title: 'cmdb.ciType.user',
          icon: 'icon-shidi-yonghu'
        },
        {
          key: BUILT_IN_TYPE.USER_GROUP,
          title: 'cmdb.ciType.userGroup',
          icon: 'ops-setting-group'
        }
      ],
      userGroupList: [],
      allFlatEmployees: [],
      form: this.$form.createForm(this),
      formLayout: {
        labelCol: { span: 5 },
        wrapperCol: { span: 16 },
      }
    }
  },
  methods: {
    setData(data) {
      this.activeKey = data?.builtin_type || BUILT_IN_TYPE.DEPARTMENT

      this.$nextTick(() => {
        this.form.setFieldsValue({
          cascade_display: data?.cascade_display ?? false,
          display_value: data?.display_value ?? undefined,
          user_group_key: data?.user_group_key ?? undefined
        })

        this.$refs.userFilterRef.setRuleList(data?.filter_rule_list || [])
      })
    },

    getData() {
      let params = {}
      this.form.validateFields({ force: true }, (err, values) => {
        if (err) {
          params.isError = true
          return
        }

        params = {
          ...values,
          builtin_type: this.activeKey,
        }

        if (this.activeKey === BUILT_IN_TYPE.USER) {
          params.filter_rule_list = this.$refs.userFilterRef.getRuleList()
        }
      })

      return params
    },

    async clickTab(key) {
      this.activeKey = key
    },
  }
}
</script>

<style lang="less" scoped>
.builtin {
  width: 100%;

  &-tab {
    padding: 4px 80px 20px;
    display: flex;
    align-items: center;
    gap: 60px;

    &-item {
      display: flex;
      align-items: center;
      justify-content: center;
      flex-direction: column;
      border: solid 1px #E4E7ED;
      border-radius: 2px;
      padding: 0 20px;
      min-width: 72px;
      height: 64px;
      cursor: pointer;

      &-icon {
        font-size: 20px;
        color: #A5A9BC;
      }

      &-title {
        font-size: 14px;
        font-weight: 400;
        line-height: 14px;
        margin-top: 4px;
      }

      &_active {
        border-color: #B1C9FF;

        .builtin-tab-item-icon {
          color: #7F97FA;
        }

        .builtin-tab-item-title {
          color: #2F54EB;
        }
      }
    }
  }

  &-department {
    display: flex;
    align-items: center;
    margin-left: 60px;

    &-icon {
      font-size: 12px;
      color: #A5A9BC;
    }

    &-tip {
      color: #4E5969;
      font-size: 14px;
      font-weight: 400;
      margin-left: 4px;
    }
  }

  &-select {
    width: 240px;
  }
}
</style>
