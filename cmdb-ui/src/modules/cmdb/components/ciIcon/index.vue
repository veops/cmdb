<template>
  <div
    v-if="icon || title"
    class="ci-icon"
    :style="{
      '--size': size + 'px'
    }"
  >
    <template v-if="icon">
      <img
        v-if="icon.split('$$')[2]"
        :src="`/api/common-setting/v1/file/${icon.split('$$')[3]}`"
      />
      <ops-icon
        v-else
        :style="{
          color: icon.split('$$')[1],
        }"
        :type="icon.split('$$')[0]"
      />
    </template>
    <span
      class="ci-icon-letter"
      v-else-if="title"
    >
      <span>
        {{ title[0].toUpperCase() }}
      </span>
    </span>
  </div>
</template>

<script>
export default {
  name: 'CIIcon',
  props: {
    icon: {
      type: String,
      default: ''
    },
    // 如果没有icon, 默认以title 的第一个字符
    title: {
      type: String,
      default: ''
    },
    size: {
      type: [String, Number],
      default: '12'
    }
  }
}
</script>

<style lang="less" scoped>
.ci-icon {
  font-size: var(--size);
  width: var(--size);
  height: var(--size);
  display: flex;
  align-items: center;
  justify-content: center;

  & > img {
    width: var(--size);
    height: var(--size);
  }

  &-letter {
    background-color: #FFFFFF;
    color: #2f54eb;
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 2px;
    box-shadow: 0px 1px 2px rgba(47, 84, 235, 0.2);

    & > span {
      transform-origin: center;
      transform: scale(0.7);
    }
  }
}
</style>
