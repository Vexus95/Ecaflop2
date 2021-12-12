import Vue from 'vue'
import VueRouter from 'vue-router'

import AddEmployeeView from '../views/AddEmployeeView.vue'
import EditEmployeeView from '../views/EditEmployeeView.vue'
import ListEmployeesView from '../views/ListEmployeesView.vue'
import ResetDatabaseView from '../views/ResetDatabaseView.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/employees',
    name: 'ListEmployees',
    component: ListEmployeesView
  },
  {
    path: '/employee/add',
    name: 'AddEmployee',
    component: AddEmployeeView
  },
  {
    path: '/employee/:id',
    name: 'EditEmployee',
    component: EditEmployeeView
  },
  {
    path: '/reset-db',
    name: 'ResetDatabase',
    component: ResetDatabaseView
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
