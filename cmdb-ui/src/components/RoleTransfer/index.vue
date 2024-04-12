<template>
  <div class="role-transfer" :style="{ height: `${height}px` }">
    <a-switch
      class="role-transfer-switch"
      v-model="isUserRole"
      :checked-children="$t('user')"
      :un-checked-children="$t('visual')"
      @change="loadRoles"
    />
    <div class="role-transfer-left">
      <a-input :placeholder="$t('placeholderSearch')" v-model="searchValue" />
      <div v-for="item in filterAllRoles" :key="item.id" @click="handleSelectedLeft(item.id)">
        <a-checkbox :checked="selectedLeft.includes(item.id)" />
        <div :title="item.name" class="role-transfer-left-role">{{ item.name }}</div>
      </div>
    </div>
    <div class="role-transfer-operation">
      <div @click="handleRight" class="operation-right"><a-icon type="right" /></div>
      <br />
      <div @click="handleLeft" class="operation-left"><a-icon type="left" /></div>
    </div>
    <div class="role-transfer-right">
      <div
        :class="{
          'role-transfer-right-item': true,
          'role-transfer-right-selected': selectedRight.includes(right),
        }"
        v-for="right in rightData"
        :key="right"
        @click="handleSelectedRight(right)"
      >
        {{ getLabel(right) }}
      </div>
    </div>
  </div>
</template>

<script>
import { searchRole } from '@/modules/acl/api/role'

export default {
  name: 'RoleTransfer',
  props: {
    height: {
      type: Number,
      default: 260,
    },
    app_id: {
      type: String,
      default: '',
      required: true,
    },
  },
  data() {
    return {
      isUserRole: false,
      allRoles: [],
      rightData: [],
      selectedLeft: [],
      selectedRight: [],
      searchValue: '',
    }
  },
  computed: {
    filterAllRoles() {
      if (this.searchValue) {
        return this.allRoles.filter((item) => item.name.toLowerCase().includes(this.searchValue.toLowerCase()))
      }
      return this.allRoles
    },
  },
  mounted() {
    this.loadRoles()
  },
  methods: {
    loadRoles() {
      searchRole({ page_size: 9999, app_id: this.app_id, user_role: Number(this.isUserRole) }).then((res) => {
        this.allRoles = res.roles
      })
    },
    handleRight() {
      this.rightData = [...new Set([...this.selectedLeft, ...this.rightData])]
      this.selectedLeft = []
      this.selectedRight = []
    },
    handleLeft() {
      this.selectedRight.forEach((id) => {
        const _idx = this.rightData.findIndex((item) => item === id)
        if (_idx > -1) {
          this.rightData.splice(_idx, 1)
        }
      })
      this.selectedRight = []
    },
    handleSelectedLeft(id) {
      const _idx = this.selectedLeft.findIndex((item) => item === id)
      if (_idx > -1) {
        this.selectedLeft.splice(_idx, 1)
      } else {
        this.selectedLeft.push(id)
      }
    },
    handleSelectedRight(id) {
      const _idx = this.selectedRight.findIndex((item) => item === id)
      if (_idx > -1) {
        this.selectedRight.splice(_idx, 1)
      } else {
        this.selectedRight.push(id)
      }
    },
    getLabel(id) {
      const _find = this.allRoles.find((item) => item.id === id)
      return _find?.name
    },
    getValues() {
      return this.rightData.map((right) => {
        const _find = this.allRoles.find((item) => item.id === right)
        return {
          id: right,
          name: _find?.name ?? right,
        }
      })
    },
  },
}
</script>

<style lang="less" scoped>
.role-transfer {
  display: flex;
  justify-content: space-between;
  position: relative;
  & &-switch {
    position: absolute;
    top: -30px;
    left: 0;
  }
  & &-left,
  & &-right {
    width: 40%;
    background-color: #f9fbff;
    border: 1px solid #e4e7ed;
    border-radius: 4px;
    height: var(--custom-height);
    overflow: auto;
  }
  & &-left {
    padding: 12px;
    > div {
      display: flex;
      align-items: center;
      height: 30px;
    }
    .role-transfer-left-role {
      display: inline-block;
      margin-left: 12px;
      overflow: hidden;
      white-space: nowrap;
      text-overflow: ellipsis;
      width: calc(100% - 30px);
      cursor: pointer;
    }
  }
  & &-right {
    padding-top: 12px;
    overflow: auto;
    .role-transfer-right-item {
      cursor: pointer;
      padding: 2px 12px;
      margin: 2px 0;
    }
    .role-transfer-right-selected {
      background-color: #f0f5ff;
    }
  }
  & &-operation {
    width: 10%;
    height: var(--custom-height);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    .operation-left,
    .operation-right {
      width: 20px;
      height: 20px;
      border-radius: 2px;
      background-color: #custom_colors[color_2];
      color: #custom_colors[color_1];
      display: inline-flex;
      justify-content: center;
      align-items: center;
      cursor: pointer;
      &:hover {
        background-color: #custom_colors[color_1];
        color: #fff;
      }
    }
  }
}
</style>
