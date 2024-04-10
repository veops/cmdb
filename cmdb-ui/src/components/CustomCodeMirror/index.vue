<template>
  <div :style="{ marginTop: '20px' }">
    <div class="codemirror-toolbar">
      <div class="codemirror-toolbar-item">
        <a class="icon" @click="changeFontSize(-1)"><a-icon type="minus-circle"/></a>
        <span> A </span>
        <a class="icon" @click="changeFontSize(1)"><a-icon type="plus-circle"/></a>
      </div>
      <div class="codemirror-toolbar-item" :style="{ position: 'absolute', right: '0' }">
        <a class="icon" @click="changeFullscreen"><a-icon type="fullscreen"/></a>
      </div>
      <div class="codemirror-toolbar-item">
        <a-select :value="keyMap" :style="{ width: '100px' }" @change="changeKeyMap">
          <a-select-option v-for="item in keyMapList" :key="item.value" :value="item.value">{{
            item.label
          }}</a-select-option>
        </a-select>
      </div>
    </div>
    <textarea :id="codeMirrorId" :style="{ width: '100%' }" />
    <div class="codemirror-toolbar-fullscreen-exit" v-if="fullscreenExitVisible" @click="changeFullscreen">
      <a-icon type="fullscreen-exit" />
    </div>
  </div>
</template>

<script>
import CodeMirror from 'codemirror'

import 'codemirror/lib/codemirror.css'
import 'codemirror/theme/monokai.css'

import 'codemirror/addon/hint/show-hint.js'
import 'codemirror/addon/hint/show-hint.css'
// import 'codemirror/addon/fold/foldcode.js'
// import 'codemirror/addon/fold/foldgutter.js'
// import 'codemirror/addon/fold/brace-fold.js'
// import 'codemirror/addon/fold/indent-fold.js'
// import 'codemirror/addon/fold/comment-fold.js'
// import 'codemirror/addon/edit/closebrackets.js'
// import 'codemirror/addon/edit/matchbrackets.js'
// import 'codemirror/addon/selection/active-line.js'

import 'codemirror/addon/display/fullscreen.js'
import 'codemirror/addon/display/fullscreen.css'

import 'codemirror/addon/dialog/dialog.js'
import 'codemirror/addon/dialog/dialog.css'
import 'codemirror/addon/search/searchcursor.js'
import 'codemirror/addon/search/search.js'
import 'codemirror/addon/search/matchesonscrollbar.css'
import 'codemirror/addon/scroll/annotatescrollbar.js'
import 'codemirror/addon/search/matchesonscrollbar.js'
import 'codemirror/addon/search/jump-to-line.js'
import 'codemirror/addon/search/match-highlighter.js'

import 'codemirror/keymap/vim.js'
import 'codemirror/keymap/emacs.js'
import 'codemirror/keymap/sublime.js'
import 'codemirror/addon/edit/matchbrackets.js'
import 'codemirror/addon/edit/closebrackets.js'
import 'codemirror/addon/comment/comment.js'
import 'codemirror/addon/wrap/hardwrap.js'
import 'codemirror/addon/fold/foldcode.js'
import 'codemirror/addon/fold/brace-fold.js'
import 'codemirror/mode/javascript/javascript.js'
import 'codemirror/mode/clike/clike.js'

require('codemirror/mode/python/python.js')
require('codemirror/mode/shell/shell.js')
require('codemirror/mode/powershell/powershell.js')

export default {
  name: 'CustomCodeMirror',
  //   props: {
  //     codeContent: {
  //       type: String,
  //       default: '',
  //     },
  //   },
  //   model: {
  //     prop: 'codeContent',
  //     event: 'change',
  //   },
  props: {
    codeMirrorId: {
      type: String,
      default: 'codemirror',
    },
  },
  data() {
    return {
      coder: null,
      fontSize: 14,
      keyMap: 'default',
      fullscreenExitVisible: false,
    }
  },
  computed: {
    keyMapList() {
      return [
        { value: 'default', label: this.$t('default') },
        { value: 'vim', label: 'vim' },
        { value: 'emacs', label: 'emacs' },
        { value: 'sublime', label: 'sublime' },
      ]
    },
  },
  mounted() {},
  methods: {
    initCodeMirror(codeContent) {
      const that = this
      if (this.coder) {
        this.coder.setValue(codeContent)
        return
      }
      this.coder = CodeMirror.fromTextArea(document.getElementById(this.codeMirrorId), {
        lineNumbers: true,
        mode: 'python',
        theme: 'monokai',
        smartIndent: true,
        tabSize: 4,
        lineWrapping: false,
        indentUnit: 4,
        extraKeys: {
          F11: function(cm) {
            that.fullscreenExitVisible = !cm.getOption('fullScreen')
            cm.setOption('fullScreen', !cm.getOption('fullScreen'))
          },
          Tab: (cm) => {
            if (cm.somethingSelected()) {
              cm.indentSelection('add')
            } else {
              cm.replaceSelection(Array(cm.getOption('indentUnit') + 1).join(' '), 'end', '+input')
            }
          },
          'Shift-Tab': (cm) => {
            if (cm.somethingSelected()) {
              cm.indentSelection('subtract')
            } else {
              const cursor = cm.getCursor()
              cm.setCursor({ line: cursor.line, ch: cursor.ch - 4 })
            }
          },

          // Esc: function(cm) {
          //   if (cm.getOption('fullScreen')) cm.setOption('fullScreen', false)
          // },
        },
        hintOptions: {
          // 自定义提示选项
          completeSingle: false, // 当匹配只有一项的时候是否自动补全
        },
      })
      const keyMap = localStorage.getItem('dagCodeMirrorKeyMap')
      if (keyMap) {
        this.changeKeyMap(keyMap)
      }
      this.coder.setValue(codeContent)
      this.coder.on('keypress', () => {
        // 显示智能提示
        this.coder.showHint()
      })
      this.coder.on('change', () => {
        this.$emit('changeCodeContent', this.coder.getValue())
      })
      this.coder.on('focus', () => {
        this.$emit('focus')
      })
    },
    changeStyle(value) {
      switch (value) {
        case '0':
          this.coder.setOption('mode', 'shell')
          break
        case '1':
          this.coder.setOption('mode', 'shell')
          break
        case '3':
          this.coder.setOption('mode', 'powershell')
          break
        case '4':
          this.coder.setOption('mode', 'ruby')
          break
        default:
          this.coder.setOption('mode', 'python')
      }
    },
    changeFontSize(num) {
      const element = document.getElementsByClassName('CodeMirror')[0]
      if (element) {
        if (num === -1 && this.fontSize <= 12) {
          return
        }
        if (num === 1 && this.fontSize >= 25) {
          return
        }
        this.fontSize = this.fontSize + num
        element.style.fontSize = `${this.fontSize}px`
      }
    },
    changeFullscreen() {
      this.fullscreenExitVisible = !this.coder.getOption('fullScreen')
      this.coder.setOption('fullScreen', !this.coder.getOption('fullScreen'))
    },
    changeKeyMap(value) {
      this.keyMap = value
      localStorage.setItem('dagCodeMirrorKeyMap', value)
      this.coder.setOption('keyMap', value)
      this.coder.setOption('matchBrackets', true)
      if (value === 'vim') {
        // var commandDisplay = document.getElementById('command-display')
        var keys = ''
        CodeMirror.on(this.coder, 'vim-keypress', function(key) {
          keys = keys + key
          // commandDisplay.innerText = keys
        })
        CodeMirror.on(this.coder, 'vim-command-done', function(e) {
          keys = ''
          // commandDisplay.innerHTML = keys
        })
        // var vimMode = document.getElementById('vim-mode')
        // CodeMirror.on(this.coder, 'vim-mode-change', function(e) {
        //   vimMode.innerText = JSON.stringify(e)
        // })
      }
    },
  },
}
</script>

<style lang="less">
.CodeMirror {
  border: 1px solid silver;
  border-width: 1px 2px;
  line-height: 150%;
  font-size: 14px;
}
.CodeMirror-hints {
  z-index: 9999;
}
.codemirror-toolbar {
  width: 100%;
  height: 34px;
  background-color: #fafafa;
  border: 1px solid #d9d9d9;
  position: relative;
  .codemirror-toolbar-item {
    display: inline-block;
    height: 30px;
    line-height: 30px;
    padding: 0 10px;
    vertical-align: text-bottom;
    .icon {
      color: #000000a6;
      &:hover {
        color: black;
      }
    }
  }
}
.codemirror-toolbar-fullscreen-exit {
  position: fixed;
  z-index: 9999;
  top: 10px;
  right: 10px;
  width: 30px;
  height: 30px;
  border-radius: 15px;
  background-color: #f3f3f3;
  text-align: center;
  line-height: 30px;
  cursor: pointer;
  &:hover {
    color: black;
  }
}
</style>
