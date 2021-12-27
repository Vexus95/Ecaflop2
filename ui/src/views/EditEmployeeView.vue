<template>
  <div>
    <EditEmployee :id='$route.params.id'/>
  </div>
</template>

<script>
import EditEmployee from '@/components/EditEmployee.vue'

export default {
  name: 'EditEmployeeView',
  components: {
    EditEmployee
  },
  props: {
    id: String
  }
}
</script>
