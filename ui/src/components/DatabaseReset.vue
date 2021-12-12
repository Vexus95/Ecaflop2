<template>
  <div>
    <p> You are about to delete the whole database</p>
    <p> This action cannot be undone</p>
    <form @submit='onSubmit'>
     <button type='submit' class='btn btn-danger'>Proceed</button>
    </form>
    <p v-if="loading">Loading ...</p>
    <p v-if="error">{{ error }}</p>
    <p v-if="success">Deleted {{ deleted }} employees</p>
  </div>
</template>

<script>
import Client from '../Client'

export default {
  name: 'DatabaseReset',
  data () {
    return {
      loading: false,
      error: '',
      success: false,
      deleted: 0
    }
  },
  methods: {
    onSubmit: async function (event) {
      event.preventDefault()
      const client = new Client(this)
      const json = await client.doRequest('/employees', { method: 'DELETE' })
      if (!json) {
        return
      }
      this.deleted = json.deleted
    }
  }
}
</script>

<style>
</style>
