<template>
  <div>
    <h2>List Employees</h2>
    <EmployeesList />
  </div>
</template>

<script>
import EmployeesList from '@/components/EmployeesList.vue'

export default {
  name: 'ListEmployeesView',
  components: {
    EmployeesList
  }
}
</script>
