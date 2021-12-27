<template>
  <div>
    <DeleteEmployee :id='$route.params.id'/>
  </div>
</template>

<script>
import DeleteEmployee from '@/components/DeleteEmployee.vue'

export default {
  name: 'DeleteEmployeeView',
  components: {
    DeleteEmployee
  },
  props: {
    id: String
  }
}
</script>
