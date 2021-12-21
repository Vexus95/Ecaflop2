<template>
<div>
  <EmployeeForm
    :initialData="initialData"
    :onSubmit="this.onSubmit"
    submitText="Add"
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
    return {
      loading: true,
      error: '',
      success: false,
      initialData: Employee.initialData()
    }
  },
  methods: {
    onSubmit: async function (payload) {
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
