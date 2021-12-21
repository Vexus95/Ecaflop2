<template>
<div id="employee-fom">
  <form @submit="submitClicked">
  <fieldset>
    <legend>
     Basic Info
    </legend>
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
    <hr>

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
      </div>
      <div class='col col-10'>
          <input
            class='form-control'
            name='address_line2'
            v-model='address_line2'
          >
        </div>
      <div class='row'>
        <div class='col col-2'>
          <label for='city' class='form-label'>City</label>
        </div>
        <div class='col col-3'>
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
      </div>
    </fieldset>
    <br>
    <button type='submit' class='btn btn-primary'>{{ submitText }}</button>
  </fieldset>
</form>
</div>
</template>

<script>
import Employee from '../Employee'

export default {
  name: 'EmployeeForm',
  props: {
    submitText: String,
    initialData: Object,
    onSubmit: Function
  },
  data: function () {
    return this.initialData
  },
  methods: {
    submitClicked: function (event) {
      event.preventDefault()
      const body = Employee.getPayloadFromElement(this)
      this.onSubmit(body)
    }
  }
}
</script>

<style>
</style>
