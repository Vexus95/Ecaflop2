<template>
<div>
  <h2>Delete  Employee</h2>
  <div v-if="employee">
  <p>
  You are about to delete records about <br />
  name: {{ employee.name }}  <br/>
  email: {{ employee.email }} <br/>
  </p>
  <p>
    This cannot be undone.
  </p>
  <form @submit='onSubmit'>
     <button type='submit' class='btn btn-danger'>Proceed</button>
  </form>
  </div>
  <p v-if="loading">Loading ...</p>
  <p v-if="error">{{ error }}</p>
</div>
</template>

<script>
import Client from '../Client'

export default {
  name: 'DeleteEmployee',
  props: {
    id: String
  },
  data: function () {
    return {
      loading: true,
      error: '',
      success: false,
      status: '',
      employee: null
    }
  },
  mounted: async function () {
    const client = new Client(this)
    const json = await client.doRequest('/employee/' + this.id)
    if (!json) {
      return
    }
    this.employee = json.employee
  },
  methods: {
    onSubmit: async function (event) {
      const client = new Client(this)
      event.preventDefault()
      console.log('deleting', this.id)
      await client.doRequest('/employee/' + this.id, { method: 'DELETE' })
      this.$router.push('/employees')
    }
  }
}
</script>

<style>
</style>
