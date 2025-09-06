import { createApp } from 'vue'
import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as echarts from 'echarts'
import router from './router'

const app = createApp(App)
app.config.globalProperties.$echarts = echarts
app.use(router).use(ElementPlus).mount('#app')