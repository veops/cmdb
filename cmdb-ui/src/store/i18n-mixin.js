import { mapState } from 'vuex'

const mixin = {
  computed: {
    ...mapState({
      currentLang: state => state.i18n.lang
    })
  },
  methods: {
    setLang (lang) {
      this.$store.dispatch('SetLang', lang)
    }
  }
}

export { mixin }
