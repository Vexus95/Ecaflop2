<template>
  <div>
    <form @submit="onSubmit">
      <fieldset>
        <legend>Basic Info</legend>
        <div class="row">
          <div class="col">
            <label for="name" class="form-label">Name</label>
          </div>
          <div class="col col-10">
            <input class="form-control" name="name" v-model="name" />
          </div>
        </div>
        <div class="row">
          <div class="col">
            <label for="email" class="form-label">Email</label>
          </div>
          <div class="col col-10">
            <input class="form-control" name="email" v-model="email" />
          </div>
        </div>
      </fieldset>
      <fieldset>
        <legend>Address</legend>
        <div class="row">
          <div class="col col-10">
            <input
              class="form-control"
              name="address_line1"
              v-model="address_line1"
            />
          </div>
          <div class="col col-10">
            <input
              class="form-control"
              name="address_line2"
              v-model="address_line2"
            />
          </div>
        </div>
        <div class="row">
          <div class="col col-2">
            <label for="city" class="form-label">City</label>
          </div>
          <div class="col col-8">
            <input class="form-control" name="city" v-model="city" />
          </div>
        </div>
        <div class="row">
          <div class="col col-2">
            <label for="zip_code" class="form-label">Zip code</label>
          </div>
          <div class="col col-3">
            <input class="form-control" name="zip_code" v-model="zip_code" />
          </div>
        </div>
      </fieldset>
      <button type='submit' class='btn btn-primary'>Add</button>
    </form>
    <span v-if="loading">loading ...</span>
    <span v-if="error">{{ error }}</span>
  </div>
</template>

<script>
import Client from '../Client'

export default {
  name: 'AddEmployee',
  data () {
    return {
      loading: false,
      error: '',
      success: false,
      name: '',
      email: '',
      address_line1: '',
      address_line2: '',
      city: '',
      zip_code: ''
    }
  },
  methods: {
    onSubmit: async function (event) {
      event.preventDefault()
      const payload = {
        name: this.name,
        email: this.email,
        address_line1: this.address_line1,
        address_line2: this.address_line2,
        city: this.city,
        zip_code: this.zip_code
      }
      const client = new Client(this)
      const json = await client.doRequest(
        '/employee',
        { method: 'PUT', body: JSON.stringify(payload) }
      )
      if (!json) {
        return
      }
      this.$router.push('/employees')
    }
  }
}
</script>

<style>
</style>
