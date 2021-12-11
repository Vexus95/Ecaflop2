<template>
  <div>
    <h2>Add Employee</h2>
    <AddEmployeeForm/>
  </div>
</template>

<script>
import AddEmployeeForm from '@/components/AddEmployeeForm.vue'

export default {
  name: 'AddEmployee',
  components: {
    AddEmployeeForm
  }
}
</script>
