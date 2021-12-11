<template>
<div id="add-employee-fom">
  <form @submit="onSubmit">
  <fieldset>
    <legend>
     Basic Info
    </legend>
    <div class='row'>
      <div class='col'>
        <label for='name' class='form-label'>Name</label>
      </div>
      <div class='col col-10'>
        <input v-model="name" name='name' class='form-control'>
      </div>
    </div>
    <div class='row'>
      <div class='col'>
        <label for='email' class='form-label'>Email</label>
      </div>
      <div class='col col-10'>
        <input v-model='email' type='email' class='form-control'>
      </div>
    </div>
    <hr>

    <fieldset>
       <legend>Address</legend>
      <div class='row'>
        <div class='col col-10'>
          <input v-model='address_line1' name='address_line1' class='form-control'>
        </div>
      </div>
      <div class='row'>
        <div class='col col-10'>
           <input v-model='address_line2' name='address_line2' class='form-control'>
        </div>
      </div>
      <div class='row'>
        <div class='col col-2'>
          <label for='city' class='form-label'>City</label>
        </div>
        <div class='col col-3'>
          <input v-model='city' class='form-control'>
        </div>
      </div>
      <div class='row'>
        <div class='col col-2'>
          <label for='zip_code' class='form-label'>Zip code</label>
        </div>
        <div class='col col-3'>
          <input v-model='zip_code' class='form-control'>
        </div>
      </div>
    </fieldset>
    <br>

    <button type='submit' class='btn btn-primary'>Submit</button>
  </fieldset>
  <span v-if="error">{{ error }}</span>
</form>
</div>
</template>

<script>
import Client from '../Client'
const fields = [
  'name',
  'email',
  'city',
  'zip_code',
  'address_line1',
  'address_line2'
]

export default {
  name: 'AddEmployeeForm',
  data () {
    const res = {
      loading: true,
      error: '',
      success: false
    }
    for (const field of fields) {
      res[field] = ''
    }
    return res
  },
  methods: {
    onSubmit: async function (event) {
      event.preventDefault()
      const client = new Client('/employee')
      await client.update(this, 'employee', fields)
      this.$router.push('/employees')
    }
  }
}
</script>

<style>
</style>
