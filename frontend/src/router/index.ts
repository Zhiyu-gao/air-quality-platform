import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import Records from '../views/Records.vue'
import Visualization from '../views/Visualization.vue'
import DataManagement from '../views/DataManagement.vue'

const routes: Array<RouteRecordRaw> = [
  { path: '/', component: Dashboard },
  { path: '/records', component: Records },
  { path: '/visualization', component: Visualization },
  { path: '/data-management', component: DataManagement },
]

export default createRouter({
  history: createWebHistory(),
  routes,
}) 