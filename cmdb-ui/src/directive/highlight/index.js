import hightlight from './highlight'

const install = function (Vue) {
    Vue.directive('hightlight', hightlight)
}

if (window.Vue) {
    window.hightlight = hightlight
    Vue.use(install); // eslint-disable-line
}
hightlight.install = install
export default hightlight
