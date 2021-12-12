<template>
<div>
  <EmployeeForm
    :onSubmit="this.onSubmit"
    :onMounted="this.onMounted"
    submitText="Add"
    v-bind:name.sync="name"
    v-bind:email.sync="email"
    v-bind:address_line1.sync="address_line1"
    v-bind:address_line2.sync="address_line2"
    v-bind:city.sync="city"
    v-bind:zip_code.sync="zip_code"
  />
</div>
</template>

<script>
import Client from '../Client'
import EmployeeForm from './EmployeeForm.vue'
import Employee from '../Employee'

export default {
  name: 'AddEmployee',
  components: {
    EmployeeForm
  },
  data () {
    return { loading: true, error: '', success: false, ...Employee.initialData() }
  },
  methods: {
    onSubmit: async function (event) {
      event.preventDefault()
      const body = Employee.updateBodyfromElement(this)
      const client = new Client(this)
      const json = await client.doRequest(
        '/employee',
        { method: 'PUT', body: JSON.stringify(body) }
      )
      if (!json) {
        return
      }
      this.$router.push('/employees')
    },
    onMounted: function () {
    }
  }
}
</script>

<style>
</style>
