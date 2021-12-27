<template>
  <div>
    <EditAddress :id='$route.params.id'/>
  </div>
</template>

<script>
import EditAddress from '@/components/EditAddress.vue'

export default {
  name: 'EditAddressView',
  components: {
    EditAddress
  },
  props: {
    id: String
  }
}
</script>
