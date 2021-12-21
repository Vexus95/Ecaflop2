<template>
<div id="employee-fom">
  <form @submit="submitClicked">
   <label for='name' class='form-label'>Name</label>
     <input
      class='form-control'
      name='name'
      v-model="name"
    >
    <button type='submit' class='btn btn-primary'>{{ submitText }}</button>
</form>
</div>
</template>

<script>
export default {
  name: 'EmployeeForm',
  props: {
    submitText: String,
    initialData: Object,
    onSubmit: Function
  },
  data: function () {
    return { name: this.initialData.name }
  },
  methods: {
    submitClicked: function (event) {
      event.preventDefault()
      this.onSubmit({ name: this.name })
    }
  }
}
</script>

<style>
</style>
