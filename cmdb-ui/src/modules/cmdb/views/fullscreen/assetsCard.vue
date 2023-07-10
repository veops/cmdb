<template>
  <div class="cmdb-fullscreen-assets">
    <div class="assets-card">
      <div class="assets-card-left">
        <div class="assets-card-left-image">
          <slot name="image1"></slot>
          <slot name="image2"></slot>
        </div>
        <slot class="assets-card-left-name" name="name"></slot>
      </div>
      <div class="assets-card-right">
        <slot name="data"></slot>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AssetsCard',
  props: {
    unit: {
      type: String,
      default: '',
    },
  },
}
</script>

<style lang="less" scoped>
.cmdb-fullscreen-assets {
  width: 100%;
  height: 100%;
  padding: 1.5em 0.5em 1em;
  .assets-card {
    width: 100%;
    height: 100%;
    background: url('../../assets/fullscreen/assets_background.png');
    background-repeat: no-repeat;
    background-size: 100% 100%;
    display: flex;
    flex-direction: row;
    color: #fff;
    &:hover .assets-card-left-image {
      > img:first-child {
        transform-origin: 0 0;
        animation: rotate 4s linear infinite;
      }
    }
    .assets-card-left,
    .assets-card-right {
      font-weight: 500;
      text-align: center;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
    }
    .assets-card-left {
      width: 40%;
      .assets-card-left-image {
        width: 100%;
        position: relative;
        height: 6em;

        > img:first-child {
          width: 3em;
          height: 3em;
          position: absolute;
          top: 1em;
          left: 50%;
          transform: translateX(-50%);
          z-index: 1;
        }
        > img:nth-child(2) {
          width: 5em;
          height: 3em;
          position: absolute;
          top: 3em;
          left: 50%;
          transform: translateX(-50%);
        }
      }
      .assets-card-left-name {
        font-size: 0.875em;
      }
    }
    .assets-card-right {
      flex: 1;
      font-size: 0.75em;
      .assets-card-right-data {
        width: 100%;
        height: 100%;
        padding: 0 1em;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        .assets-card-right-data-content {
          width: 100%;
          display: flex;
          justify-content: space-between;
          margin-bottom: 1em;
          .unit {
            color: rgba(95, 255, 245, 1);
          }
        }
        .assets-card-right-data-content:first-child {
          > span:first-child,
          > span:nth-child(2) {
            position: relative;
            &::before {
              content: '';
              position: absolute;
              width: 0.5em;
              height: 0.5em;
              border-radius: 50%;
              background-color: rgba(105, 255, 246, 0.8);
              left: -0.8em;
              top: 0.5em;
            }
          }
        }
        .assets-card-right-data-content:first-child {
          > span:nth-child(2) {
            &::before {
              background-color: rgba(105, 255, 147, 0.8);
            }
          }
        }
      }
    }
  }
}
.cmdb-fullscreen-assets:nth-child(2) {
  padding-left: 1em !important;
}
.cmdb-fullscreen-assets:last-child {
  padding-right: 1em !important;
}

@keyframes rotate {
  0% {
    transform: rotateY(0deg) translateX(-50%);
  }
  100% {
    transform: rotateY(360deg) translateX(-50%);
  }
}
</style>
