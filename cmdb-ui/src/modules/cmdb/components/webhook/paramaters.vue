<template>
  <div>
    <div class="parameters-header">
      <span>{{ $t('cmdb.components.requestParam') }}</span>
      <a-space>
        <a-tooltip :title="$t('cmdb.components.clear')">
          <ops-icon
            type="icon-xianxing-delete"
            @click="
              () => {
                parameters = []
              }
            "
          />
        </a-tooltip>
        <a-tooltip :title="$t('new')">
          <a-icon type="plus" @click="add" />
        </a-tooltip>
      </a-space>
    </div>
    <div class="parameters-box" v-if="parameters && parameters.length">
      <table>
        <tr v-for="(item, index) in parameters" :key="item.id">
          <td><a-input class="parameters-input" v-model="item.key" :placeholder="$t('cmdb.components.param', { param: `${index + 1}` })" /></td>
          <td><a-input class="parameters-input" v-model="item.value" :placeholder="$t('cmdb.components.value', { value: `${index + 1}` })" /></td>
          <td>
            <a style="color:red">
              <ops-icon type="icon-xianxing-delete" @click="deleteParam(index)" />
            </a>
          </td>
        </tr>
      </table>
    </div>
    <a-empty
      v-else
      :image-style="{
        height: '60px',
      }"
    >
      <img slot="image" :src="require('@/assets/data_empty.png')" />
      <span slot="description"> {{ $t('cmdb.components.noParamRequest') }} </span>
      <a-button @click="add" type="primary" size="small" icon="plus" class="ops-button-primary">
        {{ $t('add') }}
      </a-button>
    </a-empty>
  </div>
</template>

<script>
import { v4 as uuidv4 } from 'uuid'

export default {
  name: 'Parameters',
  data() {
    return {
      parameters: [],
    }
  },
  methods: {
    add() {
      this.parameters.push({
        id: uuidv4(),
        key: '',
        value: '',
      })
    },
    deleteParam(index) {
      this.parameters.splice(index, 1)
    },
  },
}
</script>

<style lang="less" scoped>
.parameters-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  i {
    cursor: pointer;
  }
}
.parameters-box {
  table {
    width: 100%;
    border-collapse: collapse;
  }
  table,
  td,
  th {
    border: 1px solid #f3f4f6;
  }
  .parameters-input {
    border: none;
    &:focus {
      box-shadow: none;
    }
  }
}
</style>
