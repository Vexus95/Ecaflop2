<template>
  <div>
    <EditBasic :id='$route.params.id'/>
  </div>
</template>

<script>
import EditBasic from '@/components/EditBasic.vue'

export default {
  name: 'EditBasicView',
  components: {
    EditBasic
  },
  props: {
    id: String
  }
}
</script>
