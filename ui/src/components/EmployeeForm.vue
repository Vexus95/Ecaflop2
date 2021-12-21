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
    console.log(Employee.fields)
    return { name: this.initialData.name, email: this.initialData.email }
  },
  methods: {
    submitClicked: function (event) {
      event.preventDefault()
      this.onSubmit({ name: this.name, email: this.email })
    }
  }
}
</script>

<style>
</style>
