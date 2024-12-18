<template>
  <a-popover
    v-model="visible"
    trigger="click"
    placement="bottom"
    @visibleChange="handleVisibleChange"
  >
    <div class="filter-btn">
      <a-icon class="filter-btn-icon" type="filter" />
      <span class="filter-btn-title">{{ $t('cmdb.ciType.advancedFilter') }}</span>
    </div>
    <template slot="content">
      <div class="filter-content">
        <a-form :form="form">
          <a-form-item
            :label="$t('cmdb.ciType.ciType')"
            :label-col="formLayout.labelCol"
            :wrapper-col="formLayout.wrapperCol"
          >
            <treeselect
              :value="selectCITypeIds"
              class="custom-treeselect custom-treeselect-bgcAndBorder filter-content-ciTypes"
              :style="{
                width: '400px',
                zIndex: '1000',
                '--custom-height': '32px',
                '--custom-bg-color': '#FFF',
                '--custom-border': '1px solid #d9d9d9',
                '--custom-multiple-lineHeight': '32px',
              }"
              :multiple="true"
              :clearable="true"
              searchable
              :options="CITypeGroup"
              :limit="1"
              :limitText="(count) => `+ ${count}`"
              value-consists-of="LEAF_PRIORITY"
              :placeholder="$t('cmdb.ciType.ciType')"
              @close="closeCiTypeGroup"
              @open="openCiTypeGroup"
              @input="inputCiTypeGroup"
              :normalizer="
                (node) => {
                  return {
                    id: node.id || -1,
                    label: node.alias || node.name || $t('other'),
                    title: node.alias || node.name || $t('other'),
                    children: node.ci_types,
                  }
                }
              "
            >
              <div
                :title="node.label"
                slot="option-label"
                slot-scope="{ node }"
                :style="{ width: '100%', whiteSpace: 'nowrap', textOverflow: 'ellipsis', overflow: 'hidden' }"
              >
                {{ node.label }}
              </div>
            </treeselect>
          </a-form-item>

          <a-form-item
            :label="$t('cmdb.ciType.filterPopoverLabel')"
            :label-col="formLayout.labelCol"
            :wrapper-col="formLayout.wrapperCol"
            class="filter-content-condition-filter"
          >
            <ConditionFilter
              ref="conditionFilterRef"
              :canSearchPreferenceAttrList="allAttributesList"
              :expression="expression"
              :CITypeIds="selectCITypeIds"
              :isDropdown="false"
              @setExpFromFilter="setExpFromFilter"
            />
          </a-form-item>
        </a-form>

        <div class="filter-content-action">
          <a-button
            size="small"
            @click="saveCondition(false)"
          >
            {{ $t('cmdb.ciType.saveCondition') }}
          </a-button>
          <a-button
            type="primary"
            size="small"
            @click="saveCondition(true)"
          >
            {{ $t('confirm') }}
          </a-button>
        </div>
      </div>
    </template>
  </a-popover>
</template>

<script>
import _ from 'lodash'
import ConditionFilter from '@/modules/cmdb/components/conditionFilter/index.vue'

export default {
  name: 'FilterPopover',
  components: {
    ConditionFilter
  },
  data() {
    return {
      visible: false,
      form: this.$form.createForm(this),
      formLayout: {
        labelCol: { span: 3 },
        wrapperCol: { span: 15 },
      },
      lastCiType: [],
    }
  },
  props: {
    expression: {
      type: String,
      default: ''
    },
    selectCITypeIds: {
      type: Array,
      default: () => []
    },
    CITypeGroup: {
      type: Array,
      default: () => []
    },
    allAttributesList: {
      type: Array,
      default: () => []
    }
  },
  methods: {
    handleVisibleChange(open) {
      if (open) {
        this.$nextTick(() => {
          this.$refs.conditionFilterRef.init(true, false)
        })
      }
    },
    openCiTypeGroup() {
      this.lastCiType = _.cloneDeep(this.selectCITypeIds)
    },
    closeCiTypeGroup(value) {
      if (!_.isEqual(value, this.lastCiType)) {
        this.$emit('updateAllAttributesList', value)
      }
    },
    inputCiTypeGroup(value) {
      if (!value || !value.length) {
        this.$emit('updateAllAttributesList', value)
      }
      this.$emit('changeFilter', {
        name: 'selectCITypeIds',
        value
      })
    },
    setExpFromFilter(filterExp) {
      const regSort = /(?<=sort=).+/g
      const expSort = this.expression.match(regSort) ? this.expression.match(regSort)[0] : undefined
      let expression = ''
      if (filterExp) {
        expression = `q=${filterExp}`
      }
      if (expSort) {
        expression += `&sort=${expSort}`
      }
      this.$emit('changeFilter', {
        name: 'expression',
        value: expression
      })
    },

    saveCondition(isSubmit) {
      this.$refs.conditionFilterRef.handleSubmit()
      this.$nextTick(() => {
        this.$emit('saveCondition', isSubmit, this.$parent.isColumnSearch ? 'column' : 'normal')
        this.visible = false
      })
    },
  }
}
</script>

<style lang="less" scoped>
.filter-btn {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  margin-left: 13px;
  cursor: pointer;

  &-icon {
    color: #2F54EB;
    font-size: 12px;
  }

  &-title {
    font-size: 14px;
    font-weight: 400;
    color: #2F54EB;
    margin-left: 3px;
  }
}
.filter-content {
  width: 600px;

  &-ciTypes {
    /deep/ .vue-treeselect__value-container {
      line-height: 32px;
    }
  }

  &-condition-filter {
    max-height: 250px;
    // overflow-y: auto;
    margin-bottom: 0px;
  }

  &-action {
    width: 100%;
    margin-top: 12px;
    display: flex;
    justify-content: flex-end;
    align-items: center;
    column-gap: 21px;
  }
}
</style>
