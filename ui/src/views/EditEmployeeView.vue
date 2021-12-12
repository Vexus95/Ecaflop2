<template>
  <div>
    <h2>Edit Employee</h2>
    <EditEmployee :id='$route.params.id'/>
  </div>
</template>

<script>
import EditEmployee from '@/components/EditEmployee.vue'

export default {
  name: 'EditEmployeeView',
  components: {
    EditEmployee
  }
}
</script>
