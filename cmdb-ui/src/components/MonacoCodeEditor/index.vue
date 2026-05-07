<template>
  <div :class="['monaco-editor', { 'monaco-editor_fullscreen': isFullscreen }]">
    <div class="monaco-editor-toolbar">
      <div class="monaco-editor-toolbar-left">
        <a-select
          size="small"
          :value="currentKeymap"
          class="monaco-editor-select"
          @change="changeKeymap"
        >
          <a-select-option v-for="item in keymapOptions" :key="item.value" :value="item.value">
            {{ item.label }}
          </a-select-option>
        </a-select>
        <a-select
          size="small"
          :value="currentTheme"
          class="monaco-editor-select"
          @change="changeTheme"
        >
          <a-select-option v-for="item in themeOptions" :key="item.value" :value="item.value">
            {{ item.label }}
          </a-select-option>
        </a-select>
      </div>
      <div class="monaco-editor-toolbar-right">
        <a-tooltip :title="$t('editorDecreaseFont')">
          <a-button size="small" icon="minus" @click="changeFontSize(-1)" />
        </a-tooltip>
        <span class="monaco-editor-font-size">{{ fontSize }}</span>
        <a-tooltip :title="$t('editorIncreaseFont')">
          <a-button size="small" icon="plus" @click="changeFontSize(1)" />
        </a-tooltip>
        <a-tooltip :title="$t('editorWordWrap')">
          <a-button
            size="small"
            :type="wordWrap ? 'primary' : 'default'"
            icon="swap"
            @click="toggleWordWrap"
          />
        </a-tooltip>
        <a-tooltip :title="$t('editorFormat')">
          <a-button size="small" icon="code" @click="formatDocument" />
        </a-tooltip>
        <a-tooltip :title="isFullscreen ? $t('editorExitFullscreen') : $t('editorFullscreen')">
          <a-button size="small" :icon="isFullscreen ? 'fullscreen-exit' : 'fullscreen'" @click="toggleFullscreen" />
        </a-tooltip>
      </div>
    </div>
    <div ref="editor" class="monaco-editor-main" :style="{ height: editorHeight }"></div>
    <div v-show="currentKeymap === 'vim'" ref="vimStatus" class="monaco-editor-vim-status"></div>
  </div>
</template>

<script>
import * as monaco from 'monaco-editor/esm/vs/editor/editor.api'
import { initVimMode } from 'monaco-vim'

const DEFAULT_STORAGE_KEY = 'monacoEditorConfig'

export default {
  name: 'MonacoCodeEditor',
  model: {
    prop: 'value',
    event: 'input'
  },
  props: {
    value: {
      type: String,
      default: ''
    },
    language: {
      type: String,
      default: 'python'
    },
    height: {
      type: [String, Number],
      default: 360
    },
    readOnly: {
      type: Boolean,
      default: false
    },
    storageKey: {
      type: String,
      default: DEFAULT_STORAGE_KEY
    }
  },
  data() {
    const localConfig = this.getLocalConfig()
    return {
      editor: null,
      model: null,
      vimMode: null,
      isChangingValue: false,
      isFullscreen: false,
      currentLanguage: this.language || 'python',
      currentTheme: localConfig.theme || 'vs-dark',
      currentKeymap: localConfig.keymap || 'default',
      fontSize: localConfig.fontSize || 14,
      wordWrap: localConfig.wordWrap ?? false,
    }
  },
  computed: {
    editorHeight() {
      if (this.isFullscreen) {
        return 'calc(100vh - 82px)'
      }
      return typeof this.height === 'number' ? `${this.height}px` : this.height
    },
    keymapOptions() {
      return [
        { value: 'default', label: this.$t('default') },
        { value: 'vim', label: 'Vim' },
      ]
    },
    themeOptions() {
      return [
        { value: 'vs-dark', label: 'Dark' },
        { value: 'vs', label: 'Light' },
      ]
    }
  },
  watch: {
    value(value) {
      if (!this.editor || this.editor.getValue() === value) {
        return
      }
      this.isChangingValue = true
      this.editor.setValue(value || '')
      this.isChangingValue = false
    },
    language(value) {
      if (!value || value === this.currentLanguage) {
        return
      }
      this.changeLanguage(value)
    },
    readOnly(value) {
      if (this.editor) {
        this.editor.updateOptions({ readOnly: value })
      }
    },
    height() {
      this.layoutEditor()
    },
    isFullscreen() {
      this.layoutEditor()
    }
  },
  mounted() {
    this.initEditor()
  },
  beforeDestroy() {
    this.disposeVimMode()
    if (this.editor) {
      this.editor.dispose()
    }
    if (this.model) {
      this.model.dispose()
    }
  },
  methods: {
    initEditor() {
      this.model = monaco.editor.createModel(this.value || '', this.currentLanguage)
      this.editor = monaco.editor.create(this.$refs.editor, {
        model: this.model,
        theme: this.currentTheme,
        fontSize: this.fontSize,
        tabSize: 4,
        insertSpaces: true,
        automaticLayout: true,
        minimap: { enabled: true },
        scrollBeyondLastLine: false,
        readOnly: this.readOnly,
        wordWrap: this.wordWrap ? 'on' : 'off',
        renderLineHighlight: 'all',
        roundedSelection: false,
      })
      this.editor.onDidChangeModelContent(() => {
        if (this.isChangingValue) {
          return
        }
        this.$emit('input', this.editor.getValue())
        this.$emit('change', this.editor.getValue())
      })
      this.editor.onDidBlurEditorText(() => {
        this.$emit('blur')
      })
      this.editor.onDidFocusEditorText(() => {
        this.$emit('focus')
      })
      this.changeKeymap(this.currentKeymap, false)
    },
    getLocalConfig() {
      try {
        return JSON.parse(localStorage.getItem(this.storageKey) || '{}')
      } catch (error) {
        return {}
      }
    },
    saveLocalConfig() {
      localStorage.setItem(this.storageKey, JSON.stringify({
        theme: this.currentTheme,
        keymap: this.currentKeymap,
        fontSize: this.fontSize,
        wordWrap: this.wordWrap,
      }))
    },
    layoutEditor() {
      this.$nextTick(() => {
        if (this.editor) {
          this.editor.layout()
        }
      })
    },
    changeLanguage(language) {
      this.currentLanguage = language
      if (this.model) {
        console.log('changeLanguage', language)
        monaco.editor.setModelLanguage(this.model, language)
      }
      this.saveLocalConfig()
    },
    changeTheme(theme) {
      this.currentTheme = theme
      monaco.editor.setTheme(theme)
      this.saveLocalConfig()
    },
    changeKeymap(keymap, shouldSave = true) {
      this.currentKeymap = keymap
      this.disposeVimMode()
      if (keymap === 'vim' && this.editor) {
        this.$nextTick(() => {
          this.vimMode = initVimMode(this.editor, this.$refs.vimStatus)
        })
      }
      if (shouldSave) {
        this.saveLocalConfig()
      }
    },
    disposeVimMode() {
      if (this.vimMode) {
        this.vimMode.dispose()
        this.vimMode = null
      }
    },
    changeFontSize(offset) {
      const nextFontSize = Math.min(24, Math.max(12, this.fontSize + offset))
      this.fontSize = nextFontSize
      if (this.editor) {
        this.editor.updateOptions({ fontSize: nextFontSize })
      }
      this.saveLocalConfig()
    },
    toggleWordWrap() {
      this.wordWrap = !this.wordWrap
      if (this.editor) {
        this.editor.updateOptions({ wordWrap: this.wordWrap ? 'on' : 'off' })
      }
      this.saveLocalConfig()
    },
    formatDocument() {
      if (this.editor) {
        const formatAction = this.editor.getAction('editor.action.formatDocument')
        if (formatAction) {
          formatAction.run()
        }
      }
    },
    toggleFullscreen() {
      this.isFullscreen = !this.isFullscreen
    },
    focus() {
      if (this.editor) {
        this.editor.focus()
      }
    },
    getValue() {
      return this.editor ? this.editor.getValue() : ''
    },
    setValue(value) {
      if (this.editor) {
        this.editor.setValue(value || '')
      }
    }
  }
}
</script>

<style lang="less" scoped>
.monaco-editor {
  border: 1px solid @border-color-base;
  border-radius: 4px;
  background: #ffffff;
  overflow: hidden;

  &_fullscreen {
    position: fixed;
    z-index: 2000;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    border-radius: 0;
  }

  &-toolbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    padding: 8px;
    border-bottom: 1px solid @border-color-base;
    background: #f7f8fa;
    overflow: auto;
  }

  &-toolbar-left,
  &-toolbar-right {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  &-select {
    width: 116px;
  }

  &-font-size {
    min-width: 28px;
    color: @text-color_3;
    text-align: center;
    font-size: 12px;
  }

  &-main {
    width: 100%;
  }

  &-vim-status {
    min-height: 24px;
    padding: 3px 8px;
    border-top: 1px solid @border-color-base;
    background: #1e1e1e;
    color: #d4d4d4;
    font-family: Menlo, Monaco, Consolas, 'Courier New', monospace;
    font-size: 12px;
  }
}
</style>
