<template>
<div>
  <EmployeeForm
    :onSubmit="this.onSubmit"
    :onMounted="this.onMounted"
    submitText="Save"
    v-bind:name.sync="name"
    v-bind:email.sync="email"
    v-bind:address_line1.sync="address_line1"
    v-bind:address_line2.sync="address_line2"
    v-bind:city.sync="city"
    v-bind:zip_code.sync="zip_code"
  />
  <span>{{ status }}</span>
</div>
</template>

<script>
import EmployeeForm from './EmployeeForm.vue'
import Client from '../Client'
import Employee from '../Employee'

export default {
  name: 'EditEmployee',
  props: ['id'],
  components: {
    EmployeeForm
  },
  data () {
    return {
      loading: true,
      error: '',
      success: false,
      status: '',
      ...Employee.initialData()
    }
  },
  methods: {
    url: function () {
      return '/employee/' + this.id
    },
    onSubmit: async function (event) {
      event.preventDefault()
      this.status = 'Saving ...'
      const body = Employee.updateBodyfromElement(this)
      const client = new Client(this)
      const json = await client.doRequest(
        this.url(),
        { method: 'PUT', body: JSON.stringify(body) }
      )
      if (!json) {
        this.status = ''
        return
      }
      this.status = 'Saved'
    },
    onMounted: async function () {
      const client = new Client(this)
      const json = await client.doRequest(this.url())
      if (!json) {
        return
      }
      Employee.updateElementFromJson(this, json.employee)
    }
  }
}
</script>

<style>
</style>
