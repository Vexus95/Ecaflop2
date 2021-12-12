<template>
<div id="employee-fom">
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
        <input
          class='form-control'
          name='name'
          v-bind:value="name"
          v-on:input="$emit('update:name', $event.target.value)"
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
          v-bind:value="email"
          v-on:input="$emit('update:email', $event.target.value)"
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
            v-bind:value='address_line1'
            v-on:input="$emit('update:address_line1', $event.target.value)"
          >
        </div>
      </div>
      <div class='col col-10'>
          <input
            class='form-control'
            name='address_line2'
            v-bind:value='address_line2'
            v-on:input="$emit('update:address_line2', $event.target.value)"
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
            v-bind:value='city'
            v-on:input="$emit('update:city', $event.target.value)"
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
            v-bind:value='zip_code'
            v-on:input="$emit('update:zip_code', $event.target.value)"
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
export default {
  name: 'EmployeeForm',
  props: {
    onSubmit: Function,
    onMounted: Function,
    submitText: String,
    name: String,
    email: String,
    address_line1: String,
    address_line2: String,
    city: String,
    zip_code: String
  },
  async mounted () {
    this.onMounted()
  }
}
</script>

<style>
</style>
