<template>
  <li class="ops-setting-companystructure-sidebar-tree">
    <div
      :class="{
        'ops-setting-companystructure-sidebar-group-tree-item': true,
        'ops-setting-companystructure-sidebar-group-tree-line': showLine,
        isSelected: activeId === TreeData.id || asFatherSelected,
      }"
    >
      <div class="ops-setting-companystructure-sidebar-group-tree-info" @click.stop="selectItem(TreeData)">
        <!-- <div class="info-title"> -->
        <span :title="TreeData.title">
          <ops-icon :style="{ marginRight: '8px' }" :type="icon" />
          {{ TreeData.title }}
        </span>
        <!-- </div> -->
        <!-- <span class="item-title"
          :title="TreeData.title"
        ><ops-icon :style="{ marginRight: '8px' }" :type="icon" />{{ TreeData.title }}{{ TreeData.count }}</span
        > -->
        <div class="ops-setting-companystructure-sidebar-group-tree-info-count-toggle">
          <div class="item-count-before">{{ TreeData.count }}</div>
          <!-- 显示折叠展开的图标，如果没有下级目录的话，则不显示 -->
          <div class="item-folder">
            <span v-if="isFolder" @click.stop="toggle">
              <a-icon :style="{ color: '#a1bcfb' }" :type="open ? 'up-circle' : 'down-circle'" theme="filled" />
            </span>
          </div>
        </div>
      </div>
      <ul v-if="isFolder && open" :style="{ marginLeft: '12px' }">
        <draggable v-model="TreeData.children" @end="handleEndDrag(TreeData.children)" :disabled="!isEditable">
          <CategroyTree
            v-for="(SubTree, SubIndex) in TreeData.children"
            :id="SubTree.id"
            :key="SubTree.id"
            :TreeData="SubTree"
            :showLine="SubIndex !== TreeData.children.length - 1"
            icon="setting-structure-depart2"
          />
        </draggable>
      </ul>
    </div>
  </li>
</template>

<script>
import draggable from 'vuedraggable'
import Bus from '@/views/setting/companyStructure/eventBus/bus'
import { updateDepartmentsSort } from '@/api/company'
import { mixinPermissions } from '@/utils/mixin'
export default {
  name: 'CategroyTree',
  mixins: [mixinPermissions],
  components: { draggable },
  props: {
    TreeData: {
      type: Object,
      required: true,
    },
    showLine: {
      type: Boolean,
    },
    icon: {
      type: String,
      default: 'setting-structure-depart2',
    },
  },
  data() {
    return {
      // 默认不显示下级目录
      open: false,
      activeId: null,
      asFatherSelected: false,
      // isClick: 'item-count-before',
    }
  },
  computed: {
    // 控制是否有下级目录和显示下级目录
    isFolder() {
      return this.TreeData.hasSub
    },
    isEditable() {
      return this.hasDetailPermission('backend', '公司架构', ['update'])
    },
  },
  created() {
    Bus.$on('changeActiveId', (cid) => {
      this.activeId = cid
    })
    Bus.$on('asFatherSelected', (cid) => {
      this.fatherSelected(cid)
    })
    Bus.$on('resettoggle', (isToggle) => {
      this.open = isToggle
    })
  },
  destroyed() {
    Bus.$off('changeActiveId')
    Bus.$off('asFatherSelected')
  },
  methods: {
    // 点击折叠展开的方法
    toggle() {
      if (this.isFolder) {
        this.selectItem(this.TreeData)
        if (!this.open) {
          Bus.$emit('reqChildren')
        }
        this.open = !this.open
      }
    },
    selectItem(selectDepartment) {
      Bus.$emit('selectDepartment', selectDepartment)
      this.activeId = selectDepartment.id
      Bus.$emit('changeActiveId', selectDepartment.id)
      Bus.$emit('asFatherSelected', this.TreeData.id)
    },
    fatherSelected(childId) {
      this.asFatherSelected = this.ownIdInChildren(childId, this.TreeData, false)
    },
    ownIdInChildren(cid, TreeData, flag = false) {
      if (TreeData.children) {
        if (TreeData.children.map((item) => item.id).includes(cid)) {
          flag = true
          return true
        } else {
          return TreeData.children
            .map((item) => {
              return this.ownIdInChildren(cid, item, flag)
            })
            .includes(true)
        }
      } else {
        return flag
      }
    },
    handleEndDrag(data) {
      updateDepartmentsSort({
        department_list: data.map((item, index) => {
          return { id: item.id, sort_value: index }
        }),
      }).then(() => {
        Bus.$emit('updateAllIncludeDepartment')
      })
    },
    // mouseOver: function() {
    //         this.isClick = 'item-count-after'
    //   },
    // mouseLeave: function() {
    //       this.isClick = 'item-count-before'
    // },
  },
}
</script>

<style lang="less">
@import '~@/style/static.less';
ul,
li {
  list-style: none;
  margin: 0;
  padding: 0;
}
.ops-setting-companystructure-sidebar-tree {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  min-height: 30px;
  position: relative;
  // padding: 7px 0 7px 10px;
  padding-left: 10px;
  color: rgba(0, 0, 0, 0.7);
  font-size: 14px;
  .ops-setting-companystructure-sidebar-group-tree-info:hover {
    color: #custom_colors[color_1];
    > .ops-setting-companystructure-sidebar-group-tree-info::before {
      background-color: #custom_colors[color_1];
    }
  }
  // .ops-setting-companystructure-sidebar-group-tree-info:first-child::before {
  //   content: '';
  //   position: absolute;
  //   top: 50%;
  //   left: 0;
  //   transform: translateY(-50%);
  //   display: inline-block;
  //   width: 5px;
  //   height: 5px;
  //   background-color: #cacaca;
  //   border-radius: 50%;
  // }
  .ops-setting-companystructure-sidebar-group-tree-item {
    display: inline-block;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    width: 100%;
    cursor: pointer;
    user-select: none;

    .ops-setting-companystructure-sidebar-group-tree-info {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 100%;
      position: relative;
      display: flex;
      justify-content: space-between;
      margin-bottom: 10px;
      > span:first-child {
        font-size: 15px;
        display: inline-block;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        width: calc(100% - 14px - 15px);
        // margin-bottom: 10px;
        // line-height: 10px;
        //   height: 5%;
      }
      .info-title {
        display: flex;
        align-items: center;
        justify-content: center;
        //   > span:first-child {
        //   font-size: 15px;
        //   display: inline-block;
        //   white-space: nowrap;
        //   overflow: hidden;
        //   text-overflow: ellipsis;
        //   width: calc(100% - 14px - 15px);
        //   margin-bottom: 10px;
        // }
      }
      //flex-wrap: wrap;
      // align-items: center;
      // .item-title{
      //   display: inline-block;
      //   white-space: nowrap;
      //   overflow: hidden;
      //   text-overflow: ellipsis;
      // }
      .item-count-after {
        //position: absolute;
        display: inline-block;
        margin: 0 auto;
        width: 27px;
        height: 15px;
        background: #ffffff;
        border-radius: 2px;
        text-align: center;
        font-family: 'Inter';
        font-style: normal;
        font-weight: 400;
        font-size: 10px;
        line-height: 12px;
        color: #2f54eb;
      }
      .ops-setting-companystructure-sidebar-group-tree-info-count-toggle {
        display: flex;
        align-items: center;
        justify-content: center;
        .item-count-before {
          display: flex;
          align-items: center;
          justify-content: center;
          //  display: inline-block;
          margin: 0 auto;
          width: 27px;
          height: 15px;
          background: #e1efff;
          border-radius: 2px;
          text-align: center;
          font-family: 'Inter';
          font-style: normal;
          font-weight: 400;
          font-size: 10px;
          line-height: 12px;
          color: #9094a6;
          margin-right: 5px;
        }
        .item-folder {
          display: flex;
          align-items: center;
          justify-content: center;
          width: 14px;
          height: 14px;
          //  // display: inline-block;
          //   justify-content: center;
          //   align-items: center;
        }
      }
      // > span:nth-child(2) {
      //   color: #a1bcfb!important;
      // }
    }
  }
  // .ops-setting-companystructure-sidebar-group-tree-line::after {
  //   content: '';
  //   position: absolute;
  //   width: 1px;
  //   height: 100%;
  //   background-color: rgba(0, 0, 0, 0.1);
  //   top: 12px;
  //   left: 12px;
  // }
  .isSelected {
    color: #2f54eb;
    > .ops-setting-companystructure-sidebar-group-tree-info {
      > span:nth-child(2) > i {
        color: #a1bcfb !important;
      }
    }
    > .ops-setting-companystructure-sidebar-group-tree-info::before {
      background-color: #custom_colors[color_1];
    }
  }
}
</style>
