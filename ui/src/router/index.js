import Vue from 'vue'
import VueRouter from 'vue-router'

import AddEmployee from '../views/AddEmployee.vue'
import EditEmployee from '../views/EditEmployee.vue'
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
    path: '/employee/add',
    name: 'AddEmployee',
    component: AddEmployee
  },
  {
    path: '/employee/:id',
    name: 'EditEmployee',
    component: EditEmployee
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
