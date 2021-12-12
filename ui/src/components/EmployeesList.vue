<template>
  <div class="employees-list">
    <span v-if="loading">Loading ...</span>
    <span v-if="error">{{ error }}</span>
    <div v-if="success">
      <h3>Employees ({{ employees.length }})</h3>
      <table class="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>email</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="employee in employees" :key="employee.id">
            <td>
               <router-link
                 :to="{path : 'employee/' + employee.id }"
                >
                {{ employee.id }}
                </router-link>
            </td>
            <td>{{ employee.name }}</td>
            <td>{{ employee.email }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <router-link to="/employee/add">Add new employee</router-link>
  </div>
</template>

<script>
import Client from '../Client'

export default {
  name: 'EmployeesList',
  data () {
    return {
      loading: true,
      error: '',
      success: false,
      employees: []
    }
  },
  async mounted () {
    const client = new Client(this)
    const json = await client.doRequest('/employees')
    if (!json) {
      return
    }
    this.employees = json.employees
  }
}
</script>

<style>
</style>
