<template>
  <div>
    <h2>Reset Database</h2>
    <DatabaseReset />
  </div>
</template>

<script>
import DatabaseReset from '@/components/DatabaseReset.vue'

export default {
  name: 'ResetDatabaseView',
  components: {
    DatabaseReset
  }
}
</script>
