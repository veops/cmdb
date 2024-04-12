<template>
  <div class="notice-content">
    <div class="notice-content-main">
      <Toolbar
        :editor="editor"
        :defaultConfig="{
          excludeKeys: [
            'emotion',
            'group-image',
            'group-video',
            'insertTable',
            'codeBlock',
            'blockquote',
            'fullScreen',
          ],
        }"
        mode="default"
      />
      <Editor class="notice-content-editor" :defaultConfig="editorConfig" mode="simple" @onCreated="onCreated" />
      <div class="notice-content-sidebar">
        <template v-if="needOld">
          <div class="notice-content-sidebar-divider">{{ $t('cmdb.components.beforeChange') }}</div>
          <div
            @dblclick="dblclickSidebar(`old_${attr.name}`, attr.alias || attr.name)"
            class="notice-content-sidebar-item"
            v-for="attr in attrList"
            :key="`old_${attr.id}`"
            :title="attr.alias || attr.name"
          >
            {{ attr.alias || attr.name }}
          </div>
          <div class="notice-content-sidebar-divider">{{ $t('cmdb.components.afterChange') }}</div>
        </template>
        <div
          @dblclick="dblclickSidebar(attr.name, attr.alias || attr.name)"
          class="notice-content-sidebar-item"
          v-for="attr in attrList"
          :key="attr.id"
          :title="attr.alias || attr.name"
        >
          {{ attr.alias || attr.name }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import _ from 'lodash'
import '@wangeditor/editor/dist/css/style.css'
import { Editor, Toolbar } from '@wangeditor/editor-for-vue'
export default {
  name: 'NoticeContent',
  components: { Editor, Toolbar },
  props: {
    attrList: {
      type: Array,
      default: () => [],
    },
    needOld: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      editor: null,
      editorConfig: { placeholder: this.$t('cmdb.components.noticeContentTips'), readOnly: this.readOnly },
      content: '',
      defaultParams: [],
      value2LabelMap: {},
    }
  },
  beforeDestroy() {
    const editor = this.editor
    if (editor == null) return
    editor.destroy() // When the component is destroyed, destroy the editor in time
  },
  methods: {
    onCreated(editor) {
      this.editor = Object.seal(editor) // Be sure to use Object.seal(), otherwise an error will be reported
    },
    getContent() {
      const html = _.cloneDeep(this.editor.getHtml())
      const _html = html.replace(
        /<span data-w-e-type="attachment" (data-w-e-is-void|data-w-e-is-void="") (data-w-e-is-inline|data-w-e-is-inline="").*?<\/span>/gm,
        (value) => {
          const _match = value.match(/(?<=data-attachment(V|v)alue=").*?(?=")/)
          return `{{${_match[0]}}}`
        }
      )
      return { body_html: html, body: _html }
    },
    setContent(html) {
      this.editor.setHtml(html)
    },
    dblclickSidebar(value, label) {
      if (!this.readOnly) {
        this.editor.restoreSelection()

        const node = {
          type: 'attachment',
          attachmentValue: value,
          attachmentLabel: `${label}`,
          children: [{ text: '' }],
        }
        this.editor.insertNode(node)
      }
    },
  },
}
</script>

<style lang="less" scoped>
.notice-content {
  width: 100%;
  & &-main {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    position: relative;
    .notice-content-editor {
      height: 300px;
      width: 75%;
      border: 1px solid #e4e7ed;
      border-top: none;
      overflow: hidden;
    }
    .notice-content-sidebar {
      width: 25%;
      position: absolute;
      height: 300px;
      bottom: 0;
      left: 0;
      border: 1px solid #e4e7ed;
      border-top: none;
      border-right: none;
      overflow: auto;
      .notice-content-sidebar-divider {
        position: sticky;
        top: 0;
        margin: 0;
        font-size: 12px;
        color: #afafaf;
        background-color: #fff;
        line-height: 20px;
        padding-left: 12px;
        &::before,
        &::after {
          content: '';
          position: absolute;
          border-top: 1px solid #d1d1d1;
          top: 50%;
          transition: translateY(-50%);
        }
        &::before {
          left: 3px;
          width: 5px;
        }
        &::after {
          right: 3px;
          width: 78px;
        }
      }
      .notice-content-sidebar-item:first-child {
        margin-top: 10px;
      }
      .notice-content-sidebar-item {
        line-height: 1.5;
        padding: 4px 12px;
        cursor: pointer;
        user-select: none;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        &:hover {
          background-color: #custom_colors[color_2];
          color: #custom_colors[color_1];
        }
      }
    }
  }
}
</style>

<style lang="less">

.notice-content {
  .w-e-bar {
    background-color: #custom_colors[color_2];
  }
  .w-e-text-placeholder {
    line-height: 1.5;
  }
}
</style>
