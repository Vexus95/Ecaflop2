<template>
  <div>
    <h2>Edit Employee</h2>
    <EmployeeForm :id='$route.params.id'/>
  </div>
</template>

<script>
import EmployeeForm from '@/components/EmployeeForm.vue'

export default {
  name: 'EditEmployee',
  components: {
    EmployeeForm
  }
}
</script>
