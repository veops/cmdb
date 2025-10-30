<template>
  <div class="advanced-config">
    <a-form-model
      :model="internalConfig"
      :label-col="{ span: 4 }"
      :wrapper-col="{ span: 18 }"
    >
      <!-- Asset Naming Template -->
      <a-form-model-item required :label="$t('cmdb.ciType.onetermSync.assetNameTemplate')">
        <a-input
          v-model="internalConfig.asset_name_template"
          :placeholder="$t('cmdb.ciType.onetermSync.assetNameTemplatePlaceholder')"
          @blur="emitChange"
        >
          <a-icon slot="prefix" type="font-size" />
        </a-input>
        <div class="ant-form-explain">
          {{ $t('cmdb.ciType.onetermSync.assetNameTemplateDesc') }}
        </div>
        <div class="ant-form-explain">
          {{ $t('cmdb.ciType.onetermSync.templateVariableTip') }}
        </div>
        <div v-if="loadingAttributes" style="margin-top: 8px;">
          <a-spin size="small" />
          <span style="margin-left: 8px;" class="ant-form-explain">{{ $t('cmdb.ciType.onetermSync.loadingAttributes') }}</span>
        </div>
        <div v-else-if="commonVariables.length" style="margin-top: 8px; line-height: 24px;">
          <a-tooltip
            v-for="variable in commonVariables"
            :key="variable.name"
            :title="`${variable.alias} (${variable.name})`"
          >
            <a-tag
              color="blue"
              style="margin: 4px 4px 0 0; cursor: pointer;"
              @click="insertVariable(variable.name)"
            >
              {{ variable.alias }}
            </a-tag>
          </a-tooltip>
        </div>
        <div v-else style="margin-top: 8px; line-height: 24px;">
          <span class="ant-form-explain">{{ $t('cmdb.ciType.onetermSync.noAvailableAttributes') }}</span>
        </div>
        <div v-if="templatePreview" style="margin-top: 8px;">
          <a-icon type="bulb" theme="filled" style="color: #faad14; margin-right: 4px;" />
          <span class="ant-form-explain">
            {{ $t('cmdb.ciType.onetermSync.previewResult') }}: <span :style="{ fontWeight: 500 }">{{ templatePreview }}</span>
          </span>
        </div>
      </a-form-model-item>

      <!-- Asset Directory Rule -->
      <a-form-model-item required :label="$t('cmdb.ciType.onetermSync.assetDirectoryRule')">
        <a-radio-group v-model="internalConfig.folder_rule.type" @change="handleRuleTypeChange">
          <a-radio value="fixed">
            <a-icon type="folder" style="margin-right: 4px;" />
            {{ $t('cmdb.ciType.onetermSync.fixedDirectory') }}
          </a-radio>
          <a-radio value="ci_attribute" style="margin-left: 24px;">
            <a-icon type="tags" style="margin-right: 4px;" />
            {{ $t('cmdb.ciType.onetermSync.byCIAttribute') }}
          </a-radio>
          <a-radio value="ci_relation" style="margin-left: 24px;">
            <a-icon type="apartment" style="margin-right: 4px;" />
            {{ $t('cmdb.ciType.onetermSync.byCIRelation') }}
          </a-radio>
        </a-radio-group>
        <div v-if="internalConfig.folder_rule.type === 'fixed'" class="ant-form-explain">
          {{ $t('cmdb.ciType.onetermSync.fixedDirectoryDesc') }}
        </div>
        <div v-else-if="internalConfig.folder_rule.type === 'ci_attribute'" class="ant-form-explain">
          {{ $t('cmdb.ciType.onetermSync.ciAttributeDesc') }}
        </div>
        <div v-else-if="internalConfig.folder_rule.type === 'ci_relation'" class="ant-form-explain">
          {{ $t('cmdb.ciType.onetermSync.ciRelationDesc') }}
        </div>

        <!-- Fixed Directory Config -->
        <div v-if="internalConfig.folder_rule.type === 'fixed'" style="margin-top: 12px;">
          <a-tree-select
            v-model="internalConfig.folder_rule.parent_id"
            style="width: 400px;"
            :dropdown-style="{ maxHeight: '400px', overflow: 'auto' }"
            :tree-data="onetermNodeTree"
            :placeholder="$t('cmdb.ciType.onetermSync.selectDirectory')"
            :load-data="loadOnetermNodes"
            tree-default-expand-all
            @change="emitChange"
          >
            <a-icon slot="suffixIcon" type="folder" />
          </a-tree-select>
          <a-button
            type="link"
            size="small"
            icon="reload"
            @click="reloadOnetermNodes"
            style="margin-left: 8px;"
          >
            {{ $t('cmdb.ciType.onetermSync.refreshDirectory') }}
          </a-button>
        </div>

        <!-- CI Attribute Config -->
        <div v-if="internalConfig.folder_rule.type === 'ci_attribute'" style="margin-top: 12px;">
          <a-input
            v-model="internalConfig.folder_rule.template"
            :placeholder="$t('cmdb.ciType.onetermSync.pathTemplatePlaceholder')"
            style="width: 500px;"
            @blur="emitChange"
          >
            <a-icon slot="prefix" type="folder-open" />
          </a-input>
          <div class="ant-form-explain">
            <span v-html="pathTemplateExampleForAttribute"></span>
          </div>
        </div>

        <!-- CI Relation Config -->
        <div v-if="internalConfig.folder_rule.type === 'ci_relation'" style="margin-top: 12px;">
          <a-input
            v-model="internalConfig.folder_rule.template"
            :placeholder="$t('cmdb.ciType.onetermSync.relationTemplatePlaceholder')"
            style="width: 500px;"
            @blur="emitChange"
          >
            <a-icon slot="prefix" type="folder-open" />
          </a-input>
          <div class="ant-form-explain">
            <span v-html="pathTemplateExampleForRelation"></span>
          </div>
        </div>
      </a-form-model-item>
    </a-form-model>
  </div>
</template>

<script>
import { getCITypeAttributesById } from '@/modules/cmdb/api/CITypeAttr'
import { getCITypes } from '@/modules/cmdb/api/CIType'

export default {
  name: 'AdvancedConfig',
  props: {
    config: {
      type: Object,
      required: true,
    },
    ciTypeId: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      internalConfig: {
        asset_name_template: '',
        folder_rule: {
          type: 'fixed',
          parent_id: 0,
        },
      },
      ciTypeAttributes: [],
      parentCITypes: [],
      templatePreview: '',
      loadingAttributes: false,
      onetermNodeTree: [],
      loadingNodes: false,
    }
  },
  computed: {
    pathTemplateExampleForAttribute() {
      const example = this.$t('cmdb.ciType.onetermSync.pathTemplateExample')
      const template = this.$t('cmdb.ciType.onetermSync.attributeTemplateExample')
      return `${example} ${template}`
    },
    pathTemplateExampleForRelation() {
      const example = this.$t('cmdb.ciType.onetermSync.pathTemplateExample')
      const template = this.$t('cmdb.ciType.onetermSync.relationTemplateExample')
      return `${example} ${template}`
    },
    commonVariables() {
      if (!this.ciTypeAttributes || !this.ciTypeAttributes.length) {
        return []
      }
      // Filter out complex types that are not suitable for templates
      const simpleAttributes = this.ciTypeAttributes.filter((attr) => {
        // value_type: 0=INT, 1=FLOAT, 2=TEXT, 3=DATETIME, 4=DATE, 5=TIME, 6=JSON, 7=BOOL
        // Exclude: JSON(6), reference, attachment, multi-value, computed

        // Exclude JSON type
        if (attr.value_type === '6' || attr.value_type === 6) return false

        // Exclude attachment type
        if (attr.is_attachment) return false

        // Exclude multi-value attributes
        if (attr.is_list) return false
        if (attr.is_choice && attr.is_choice === 2) return false // multi-choice

        // Exclude reference attributes (is_link=true means it's a reference)
        if (attr.is_link) return false

        // Exclude computed attributes (they are dynamic)
        if (attr.is_computed) return false

        // Include simple types: int, float, text, datetime, date, time, bool
        return true
      })

      // Return attribute objects with name and alias, limit to 15 for display
      return simpleAttributes.slice(0, 15).map((attr) => ({
        name: attr.name,
        alias: attr.alias || attr.name,
        value_type: attr.value_type,
      }))
    },
  },
  watch: {
    config: {
      handler(val) {
        if (!val) return

        // Deep merge folder_rule to preserve user changes
        const mergedConfig = { ...this.internalConfig, ...val }
        if (val.folder_rule && this.internalConfig.folder_rule) {
          mergedConfig.folder_rule = {
            ...this.internalConfig.folder_rule,
            ...val.folder_rule,
          }
        }

        this.internalConfig = mergedConfig
        this.updateTemplatePreview()
      },
      immediate: true,
      deep: true,
    },
    'internalConfig.asset_name_template'(val) {
      this.updateTemplatePreview()
    },
  },
  mounted() {
    this.loadCITypeAttributes()
    this.loadParentCITypes()
    this.loadOnetermNodes()
  },
  methods: {
    handleRuleTypeChange() {
      if (this.internalConfig.folder_rule.type === 'fixed' && !this.onetermNodeTree.length) {
        this.loadOnetermNodes()
      }
      this.emitChange()
    },

    async loadOnetermNodes() {
      // *
    },

    reloadOnetermNodes() {
      this.onetermNodeTree = []
      this.loadOnetermNodes()
    },

    async loadCITypeAttributes() {
      this.loadingAttributes = true
      try {
        const res = await getCITypeAttributesById(this.ciTypeId)
        this.ciTypeAttributes = res.attributes || []
      } catch (e) {
        console.error('Failed to load attributes:', e)
        this.ciTypeAttributes = []
      } finally {
        this.loadingAttributes = false
      }
    },

    async loadParentCITypes() {
      try {
        const res = await getCITypes({ type_id: this.ciTypeId, parent_types: true })
        this.parentCITypes = res || []
      } catch (e) {
        console.error('Failed to load parent types:', e)
        // 如果接口不存在，加载所有CI类型
        this.loadAllCITypes()
      }
    },

    async loadAllCITypes() {
      try {
        const res = await getCITypes()
        this.parentCITypes = (res.ci_types || []).filter((t) => t.id !== this.ciTypeId)
      } catch (e) {
        console.error('Failed to load CI types:', e)
      }
    },

    insertVariable(variable) {
      const input = this.internalConfig.asset_name_template || ''
      this.internalConfig.asset_name_template = input + '{{ ' + variable + ' }}'
      this.emitChange()
    },

    updateTemplatePreview() {
      const template = this.internalConfig.asset_name_template
      if (!template) {
        this.templatePreview = ''
        return
      }

      // Generate example data based on CI Type attributes
      const exampleData = {}
      this.ciTypeAttributes.forEach((attr) => {
        // Generate example values based on attribute type
        if (attr.value_type === 'int' || attr.value_type === 'float') {
          exampleData[attr.name] = '100'
        } else if (attr.name.includes('ip') || attr.name === 'ip_address') {
          exampleData[attr.name] = '10.0.1.100'
        } else if (attr.name.includes('port')) {
          exampleData[attr.name] = '3306'
        } else if (attr.name.includes('name') || attr.name === 'hostname') {
          exampleData[attr.name] = 'server-01'
        } else if (attr.name.includes('env') || attr.name === 'environment') {
          exampleData[attr.name] = 'production'
        } else {
          exampleData[attr.name] = 'example'
        }
      })

      try {
        let preview = template

        // Handle basic Jinja2 variable substitution
        Object.keys(exampleData).forEach((key) => {
          const regex = new RegExp('\\{\\{\\s*' + key + '\\s*\\}\\}', 'g')
          preview = preview.replace(regex, exampleData[key])
        })

        // Handle common Jinja2 filters
        preview = preview.replace(/\{\{\s*(\w+)\s*\|\s*upper\s*\}\}/g, (match, key) => {
          return exampleData[key] ? exampleData[key].toUpperCase() : match
        })
        preview = preview.replace(/\{\{\s*(\w+)\s*\|\s*lower\s*\}\}/g, (match, key) => {
          return exampleData[key] ? exampleData[key].toLowerCase() : match
        })

        this.templatePreview = preview
      } catch (e) {
        this.templatePreview = 'Template error: ' + e.message
      }
    },

    emitChange() {
      this.$emit('change', this.internalConfig)
    },
  },
}
</script>
