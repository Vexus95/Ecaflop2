<template>
<div>
  <h2>Edit Basic Employee info</h2>
  <form @submit="submitClicked">
  <fieldset>
    <legend>Basic Info</legend>
    <div class='row'>
      <div class='col'>
        <label for='name' class='form-label'>Name</label>
      </div>
      <div class='col col-10'>
        <input
          class='form-control'
          name='name'
          v-model="name"
        >
      </div>
    </div>
    <div class='row'>
      <div class='col'>
        <label for='email' class='form-label'>Email</label>
      </div>
      <div class='col col-10'>
        <input
          class='form-control'
          name='email'
          v-model="email"
        >
     </div>
  </div>
  </fieldset>
  <button type='submit' class='btn btn-primary'>Update</button>
  </form>
  <span>{{ status }}</span>
  <span v-if="error">{{ error }}</span>
  <span v-if="loading">loading ...</span>
</div>
</template>

<script>
import Client from '../Client'

export default {
  name: 'EditBasic',
  props: {
    id: String
  },
  data: function () {
    return {
      loading: true,
      error: '',
      success: false,
      status: '',
      name: '',
      email: ''
    }
  },
  mounted: async function () {
    const client = new Client(this)
    const json = await client.doRequest(this.url())
    if (!json) {
      return
    }
    this.name = json.employee.name
    this.email = json.employee.email
  },
  methods: {
    url: function () {
      return '/employee/' + this.id
    },
    submitClicked: async function (event) {
      event.preventDefault()
      this.status = 'Saving ...'
      const payload = { name: this.name, email: this.email }
      const client = new Client(this)
      const json = await client.doRequest(
        this.url(),
        { method: 'PATCH', body: JSON.stringify(payload) }
      )
      if (!json) {
        this.status = ''
        return
      }
      this.$router.push('/employees')
    }
  }
}
</script>

<style>
</style>
