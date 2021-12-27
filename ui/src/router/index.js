import Vue from 'vue'
import VueRouter from 'vue-router'

import AddEmployeeView from '../views/AddEmployeeView.vue'
import EditEmployeeView from '../views/EditEmployeeView.vue'
import ListEmployeesView from '../views/ListEmployeesView.vue'
import ResetDatabaseView from '../views/ResetDatabaseView.vue'
import EditAddressView from '../views/EditAddressView.vue'
import EditBasicView from '../views/EditBasicView.vue'
import DeleteEmployeeView from '../views/DeleteEmployeeView.vue'

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
    path: '/employee/:id/basic',
    name: 'EditBasic',
    component: EditBasicView
  },
  {
    path: '/employee/:id/address',
    name: 'EditAddress',
    component: EditAddressView
  },
  {
    path: '/employee/:id/delete',
    name: 'DeleteEmployee',
    component: DeleteEmployeeView
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
