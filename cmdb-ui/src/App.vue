<template>
  <a-config-provider :locale="locale">
    <div id="app" :class="{ 'ops-fullscreen': isOpsFullScreen, 'ops-only-topmenu': isOpsOnlyTopMenu }">
      <router-view v-if="alive" />
    </div>
  </a-config-provider>
</template>

<script>
import { mapActions } from 'vuex'
import zhCN from 'ant-design-vue/lib/locale-provider/zh_CN'
import { AppDeviceEnquire } from '@/utils/mixin'
import { debounce } from './utils/util'

import { h } from 'snabbdom'
import { DomEditor, Boot } from '@wangeditor/editor'

export default {
  mixins: [AppDeviceEnquire],
  provide() {
    return {
      reload: this.reload,
    }
  },
  data() {
    return {
      locale: zhCN,
      alive: true,
      timer: null,
    }
  },
  computed: {
    isOpsFullScreen() {
      return this.$route.name === 'cmdb_screen'
    },
    isOpsOnlyTopMenu() {
      return ['fullscreen_index', 'setting_person'].includes(this.$route.name)
    },
  },
  created() {
    this.timer = setInterval(() => {
      this.setTime(new Date().getTime())
    }, 1000)
  },
  mounted() {
    this.$store.dispatch('setWindowSize')
    window.addEventListener(
      'resize',
      debounce(() => {
        this.$store.dispatch('setWindowSize')
      })
    )

    // 注册富文本自定义元素
    const resume = {
      type: 'attachment',
      attachmentLabel: '',
      attachmentValue: '',
      children: [{ text: '' }], // void 元素必须有一个 children ，其中只有一个空字符串，重要！！！
    }

    function withAttachment(editor) {
      // JS 语法
      const { isInline, isVoid } = editor
      const newEditor = editor

      newEditor.isInline = (elem) => {
        const type = DomEditor.getNodeType(elem)
        if (type === 'attachment') return true // 针对 type: attachment ，设置为 inline
        return isInline(elem)
      }

      newEditor.isVoid = (elem) => {
        const type = DomEditor.getNodeType(elem)
        if (type === 'attachment') return true // 针对 type: attachment ，设置为 void
        return isVoid(elem)
      }

      return newEditor // 返回 newEditor ，重要！！！
    }
    Boot.registerPlugin(withAttachment)
    /**
     * 渲染“附件”元素到编辑器
     * @param elem 附件元素，即上文的 myResume
     * @param children 元素子节点，void 元素可忽略
     * @param editor 编辑器实例
     * @returns vnode 节点（通过 snabbdom.js 的 h 函数生成）
     */
    function renderAttachment(elem, children, editor) {
      // JS 语法

      // 获取“附件”的数据，参考上文 myResume 数据结构
      const { attachmentLabel = '', attachmentValue = '' } = elem

      // 附件元素 vnode
      const attachVnode = h(
        // HTML tag
        'span',
        // HTML 属性、样式、事件
        {
          props: { contentEditable: false }, // HTML 属性，驼峰式写法
          style: {
            display: 'inline-block',
            margin: '0 3px',
            padding: '0 3px',
            backgroundColor: '#e6f7ff',
            border: '1px solid #91d5ff',
            borderRadius: '2px',
            color: '#1890ff',
          }, // style ，驼峰式写法
          on: {
            click() {
              console.log('clicked', attachmentValue)
            } /* 其他... */,
          },
        },
        // 子节点
        [attachmentLabel]
      )

      return attachVnode
    }
    const renderElemConf = {
      type: 'attachment', // 新元素 type ，重要！！！
      renderElem: renderAttachment,
    }
    Boot.registerRenderElem(renderElemConf)

    /**
     * 生成“附件”元素的 HTML
     * @param elem 附件元素，即上文的 myResume
     * @param childrenHtml 子节点的 HTML 代码，void 元素可忽略
     * @returns “附件”元素的 HTML 字符串
     */
    function attachmentToHtml(elem, childrenHtml) {
      // JS 语法

      // 获取附件元素的数据
      const { attachmentValue = '', attachmentLabel = '' } = elem

      // 生成 HTML 代码
      const html = `<span data-w-e-type="attachment" data-w-e-is-void data-w-e-is-inline data-attachmentValue="${attachmentValue}" data-attachmentLabel="${attachmentLabel}">${attachmentLabel}</span>`

      return html
    }
    const elemToHtmlConf = {
      type: 'attachment', // 新元素的 type ，重要！！！
      elemToHtml: attachmentToHtml,
    }
    Boot.registerElemToHtml(elemToHtmlConf)

    /**
     * 解析 HTML 字符串，生成“附件”元素
     * @param domElem HTML 对应的 DOM Element
     * @param children 子节点
     * @param editor editor 实例
     * @returns “附件”元素，如上文的 myResume
     */
    function parseAttachmentHtml(domElem, children, editor) {
      // JS 语法

      // 从 DOM element 中获取“附件”的信息
      const attachmentValue = domElem.getAttribute('data-attachmentValue') || ''
      const attachmentLabel = domElem.getAttribute('data-attachmentLabel') || ''

      // 生成“附件”元素（按照此前约定的数据结构）
      const myResume = {
        type: 'attachment',
        attachmentValue,
        attachmentLabel,
        children: [{ text: '' }], // void node 必须有 children ，其中有一个空字符串，重要！！！
      }

      return myResume
    }
    const parseHtmlConf = {
      selector: 'span[data-w-e-type="attachment"]', // CSS 选择器，匹配特定的 HTML 标签
      parseElemHtml: parseAttachmentHtml,
    }
    Boot.registerParseElemHtml(parseHtmlConf)
  },
  beforeDestroy() {
    clearInterval(this.timer)
  },
  methods: {
    ...mapActions(['setTime']),
    reload() {
      this.alive = false
      this.$nextTick(() => {
        this.alive = true
      })
    },
  },
}
</script>
<style lang="less">
@import './style/index.less';

#app {
  height: 100%;
}
</style>
