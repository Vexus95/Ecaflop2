<template>
<div>
  <h2>Edit  Employee Address</h2>
  <span v-if="loading">loading ...</span>
  <form v-else @submit="submitClicked">
  <fieldset>
    <legend>Address</legend>
      <div class='row'>
        <div class='col col-10'>
          <input
            class='form-control'
            name='address_line1'
            v-model='address_line1'
          >
        </div>
        <div class='col col-10'>
          <input
            class='form-control'
            name='address_line2'
            v-model='address_line2'
          >
        </div>
      </div>
      <div class='row'>
        <div class='col col-2'>
          <label for='city' class='form-label'>City</label>
        </div>
        <div class='col col-8'>
          <input
            class='form-control'
            name='city'
            v-model='city'
          >
        </div>
      </div>
      <div class='row'>
        <div class='col col-2'>
          <label for='zip_code' class='form-label'>Zip code</label>
        </div>
        <div class='col col-3'>
          <input
            class='form-control'
            name='zip_code'
            v-model='zip_code'
          >
        </div>
      </div>  </fieldset>
  <button type='submit' class='btn btn-primary'>Update</button>
  </form>
  <span>{{ status }}</span>
  <span v-if="error">{{ error }}</span>
</div>
</template>

<script>
import Client from '../Client'

export default {
  name: 'EditAddress',
  props: {
    id: String
  },
  data: function () {
    return {
      loading: true,
      error: '',
      success: false,
      status: '',
      address_line1: '',
      address_line2: '',
      city: '',
      zip_code: ''
    }
  },
  mounted: async function () {
    const client = new Client(this)
    const json = await client.doRequest(this.url())
    if (!json) {
      return
    }
    this.address_line1 = json.employee.address_line1
    this.address_line2 = json.employee.address_line2
    this.city = json.employee.city
    this.zip_code = json.employee.zip_code
  },
  methods: {
    url: function () {
      return '/employee/' + this.id
    },
    submitClicked: async function (event) {
      event.preventDefault()
      this.status = 'Saving ...'
      const payload = {
        address_line1: this.address_line1,
        address_line2: this.address_line2,
        city: this.city,
        zip_code: this.zip_code
      }
      const client = new Client(this)
      console.log('starting patch request ...')
      const json = await client.doRequest(
        this.url(),
        { method: 'PATCH', body: JSON.stringify(payload) }
      )
      if (!json) {
        this.status = ''
      }
      console.log('json', json)
      this.$router.push('/employees')
    }
  }
}
</script>

<style>
</style>
