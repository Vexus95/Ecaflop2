import Vue from 'vue'
import VueRouter from 'vue-router'
import ListEmployees from '../views/ListEmployees.vue'
import ResetDatabase from '../views/ResetDatabase.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/employees',
    name: 'ListEmployees',
    component: ListEmployees
  },
  {
    path: '/reset-db',
    name: 'ResetDatabase',
    component: ResetDatabase
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
