import Vue from 'vue'
import App from './App.vue'
import router from './router'
import $ from 'jquery'
import VueEvents from 'vue-events'
import Vuex from 'vuex'
import * as VeeValidate from 'vee-validate'
import Element from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'



Vue.use($)
Vue.use(VueEvents)
Vue.use(VeeValidate)
Vue.use(Vuex)
Vue.use(Element)


Vue.config.productionTip = false


new Vue({
    Element,
    router,
    render: h => h(App),
}).$mount('#app')