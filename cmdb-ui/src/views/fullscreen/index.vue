<template>
  <div class="ops-fullscreen-dashboard">
    <ul>
      <li class="ops-fullscreen-dashboard-li" v-for="item in list" :key="item.name">
        <a class="ops-fullscreen-dashboard-a" @click="goto(item.href)">
          <div class="ops-fullscreen-dashboard-image" :style="{ backgroundImage: `url('${item.image}')` }"></div>
          <h4>{{ item.name }}</h4>
        </a>
      </li>
    </ul>
  </div>
</template>

<script>
import cmdb_fullscreen from '../../assets/fullscreen/cmdb_fullscreen.png'
export default {
  name: 'Fullscreen',
  data() {
    return {
      list: [
        {
          name: 'CMDB',
          image: cmdb_fullscreen,
          href: '/cmdb/screen',
        },
      ],
    }
  },
  methods: {
    goto(href) {
      this.$router.push(href)
    },
  },
}
</script>

<style lang="less" scoped>
.ops-fullscreen-dashboard {
  position: fixed;
  left: 0;
  top: 40px;
  z-index: 150;
  width: 100%;
  padding: 24px;
  > ul {
    list-style: none;
    padding: 0;
    .ops-fullscreen-dashboard-li {
      display: inline-block;
      vertical-align: top;
      width: 25%;
      margin: 0;
      padding: 0;
      .ops-fullscreen-dashboard-a {
        &:hover .ops-fullscreen-dashboard-image {
          transform: translateY(-4px);
          border-color: transparent;
          box-shadow: 0 6px 16px #6b93e024;
        }
        .ops-fullscreen-dashboard-image {
          background-color: #fff;
          background-size: contain;
          background-repeat: no-repeat;
          background-position: center;
          border: 1px solid #f0f0f0;
          border-radius: 6px;
          overflow: hidden;
          height: calc(100vw / 7 - 20px);
          min-height: 130px;
          max-height: 280px;
          object-fit: cover;
          transition: all 0.3s;
          display: flex;
          justify-content: center;
        }
        h4 {
          margin: 16px 0 0;
          text-align: center;
          color: #101424;
          font-size: 16px;
          line-height: 22px;
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
        }
      }
    }
  }
}
</style>
