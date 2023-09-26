<template>
  <div>
    <div class="headers-header">
      <span>请求参数</span>
      <a-space>
        <a-tooltip title="清空">
          <ops-icon
            type="icon-xianxing-delete"
            @click="
              () => {
                headers = [
                  {
                    id: uuidv4(),
                    key: '',
                    value: '',
                  },
                ]
              }
            "
          />
        </a-tooltip>
        <a-tooltip title="新增">
          <a-icon type="plus" @click="add" />
        </a-tooltip>
      </a-space>
    </div>
    <div class="headers-box">
      <table>
        <tr v-for="(item, index) in headers" :key="item.id">
          <td><a-input class="headers-input" v-model="item.key" :placeholder="`参数${index + 1}`" /></td>
          <td><a-input class="headers-input" v-model="item.value" :placeholder="`值${index + 1}`" /></td>
          <td>
            <a style="color:red">
              <ops-icon type="icon-xianxing-delete" @click="deleteParam(index)" />
            </a>
          </td>
        </tr>
      </table>
    </div>
  </div>
</template>

<script>
import { v4 as uuidv4 } from 'uuid'

export default {
  name: 'Header',
  data() {
    return {
      headers: [
        {
          id: uuidv4(),
          key: '',
          value: '',
        },
      ],
    }
  },
  methods: {
    uuidv4,
    add() {
      this.headers.push({
        id: uuidv4(),
        key: '',
        value: '',
      })
    },
    deleteParam(index) {
      this.headers.splice(index, 1)
    },
  },
}
</script>

<style lang="less" scoped>
.headers-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  i {
    cursor: pointer;
  }
}
.headers-box {
  table {
    width: 100%;
    border-collapse: collapse;
  }
  table,
  td,
  th {
    border: 1px solid #f3f4f6;
  }
  .headers-input {
    border: none;
    &:focus {
      box-shadow: none;
    }
  }
}
</style>
