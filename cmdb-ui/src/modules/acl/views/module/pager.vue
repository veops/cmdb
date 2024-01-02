<template>
  <div>
    <a-row class="row" type="flex" justify="end">
      <a-col>
        <a-space align="end">
          <a-button class="left-button" size="small" :disabled="prevIsDisabled" @click="prevPage"><a-icon type="left" /></a-button>
          <a-button class="page-button" size="small">{{ currentPage }}</a-button>
          <a-button class="right-button" size="small" :disabled="nextIsDisabled" @click="nextPage"><a-icon type="right" /></a-button>
          <a-dropdown class="dropdown" size="small" placement="topCenter" :trigger="['click']" :disabled="dropdownIsDisabled">
            <a-menu slot="overlay">
              <a-menu-item v-for="(size,index) in pageSizes" :key="index" @click="handleItemClick(size)">
                {{ size }}{{ $t('itemsPerPage') }}
              </a-menu-item>
            </a-menu>
            <a-button size="small"> {{ pageSize }}{{ $t('itemsPerPage') }}<a-icon type="down" /> </a-button>
          </a-dropdown>
        </a-space>
      </a-col>
    </a-row>
  </div>
</template>

<script>
export default {
    props: {
        currentPage: {
            type: Number,
            required: true
        },
        pageSize: {
            type: Number,
            required: true
        },
        pageSizes: {
            type: Array,
            required: true
        },
        total: {
            type: Number,
            required: true
        },
        isLoading: {
            type: Boolean,
            required: false
        }
    },
    data() {
        return {
            dropdownIsDisabled: false,
            prevIsDisabled: true,
        }
    },
    computed: {
        nextIsDisabled() {
            return this.isLoading || this.total < this.pageSize
        }
    },
    watch: {
        isLoading: {
            immediate: true,
            handler: function (val) {
                if (val === true) {
                    this.dropdownIsDisabled = true
                    this.prevIsDisabled = true
                } else {
                    this.dropdownIsDisabled = false
                    if (this.currentPage === 1) {
                        this.prevIsDisabled = true
                    } else {
                        this.prevIsDisabled = false
                    }
                }
            }
        },
        currentPage: {
            immediate: true,
            handler: function (val) {
                if (val === 1) {
                    this.prevIsDisabled = true
                }
            }
        }
    },
    methods: {
        handleItemClick(size) {
            this.$emit('showSizeChange', size)
        },
        nextPage() {
            const pageNum = this.currentPage + 1
            this.$emit('change', pageNum)
        },
        prevPage() {
            const pageNum = this.currentPage - 1
            this.$emit('change', pageNum)
        }
    }
}
</script>

<style lang="less" scoped>
.row{
    margin-top: 5px;
    .left-button{
        padding: 0;
        width: 24px;
    }
    .right-button{
        padding: 0;
        width: 24px;
    }
    .page-button{
        padding: 0;
        width: 24px;
    }
}
</style>
