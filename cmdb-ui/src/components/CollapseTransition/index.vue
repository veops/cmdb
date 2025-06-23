<template>
  <transition
    :name="transitionName"
    @before-enter="collapseBeforeEnter"
    @enter="collapseEnter"
    @after-enter="collapseAfterEnter"
    @before-leave="collapseBeforeLeave"
    @leave="collapseLeave"
    @after-leave="collapseAfterLeave"
  >
    <slot></slot>
  </transition>
</template>

<script>
/**
 * Collapse transition effect for elements
 */
export default {
  name: 'CollapseTransition',
  props: {
    transitionName: {
      type: String,
      default: 'collapse-transition',
    },
  },
  data() {
    return {
      oldPaddingTop: '',
      oldPaddingBottom: '',
      oldOverflow: '',
    }
  },
  methods: {
    collapseBeforeEnter(el) {
      this.oldPaddingBottom = el.style.paddingBottom
      this.oldPaddingTop = el.style.paddingTop
      // set the element's maxHeight to 0 before the transition effect starts so that the element's maxHeight has an initial value
      el.style.paddingTop = '0'
      el.style.paddingBottom = '0'
      el.style.maxHeight = '0'
    },
    collapseEnter(el, done) {
      this.oldOverflow = el.style.overflow
      const elHeight = el.scrollHeight
      // After entering, set maxHeight to the element's height; setting maxHeight to auto will not have a transition effect
      if (elHeight > 0) {
        el.style.maxHeight = elHeight + 'px'
      } else {
        el.style.maxHeight = '0'
      }
      el.style.paddingTop = this.oldPaddingTop
      el.style.paddingBottom = this.oldPaddingBottom

      el.style.overflow = 'hidden'
      // done();
      const onTransitionDone = function() {
        done()
        el.removeEventListener('transitionend', onTransitionDone, false)
        el.removeEventListener('transitioncancel', onTransitionDone, false)
      }
      // Bind transition end event to finish Vue's transition immediately after the CSS transition
      el.addEventListener('transitionend', onTransitionDone, false)
      el.addEventListener('transitioncancel', onTransitionDone, false)
    },
    collapseAfterEnter(el) {
      // Restore maxHeight after transition is complete
      el.style.maxHeight = ''
      el.style.overflow = this.oldOverflow
    },

    collapseBeforeLeave(el) {
      this.oldPaddingBottom = el.style.paddingBottom
      this.oldPaddingTop = el.style.paddingTop
      this.oldOverflow = el.style.overflow

      el.style.maxHeight = el.scrollHeight + 'px'
      el.style.overflow = 'hidden'
    },
    collapseLeave(el, done) {
      if (el.scrollHeight !== 0) {
        el.style.maxHeight = '0'
        el.style.paddingBottom = '0'
        el.style.paddingTop = '0'
      }
      // done();
      const onTransitionDone = function() {
        done()
        el.removeEventListener('transitionend', onTransitionDone, false)
        el.removeEventListener('transitioncancel', onTransitionDone, false)
      }
      // Bind transition end event to finish Vue's transition immediately after the CSS transition
      el.addEventListener('transitionend', onTransitionDone, false)
      el.addEventListener('transitioncancel', onTransitionDone, false)
    },
    collapseAfterLeave(el) {
      el.style.maxHeight = ''
      el.style.overflow = this.oldOverflow
      el.style.paddingBottom = this.oldPaddingBottom
      el.style.paddingTop = this.oldPaddingTop

      this.oldOverflow = this.oldPaddingBottom = this.oldPaddingTop = ''
    },
  },
}
</script>

<style lang="less">
.collapse-transition-enter-active,
.collapse-transition-leave-active {
  transition: height 0.3s ease-in-out, padding 0.3s ease-in-out, max-height 0.3s ease-in-out;
}
</style>
