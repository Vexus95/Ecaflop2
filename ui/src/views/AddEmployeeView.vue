<template>
  <div>
    <h2>Add Employee</h2>
    <AddEmployee/>
  </div>
</template>

<script>
import AddEmployee from '@/components/AddEmployee.vue'

export default {
  name: 'AddEmployeeView',
  components: {
    AddEmployee
  }
}
</script>
