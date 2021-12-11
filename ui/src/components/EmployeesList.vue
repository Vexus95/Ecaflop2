<template>
  <div class="employees-list">
    <span v-if="loading">Loading ...</span>
    <span v-if="error">{{ error }}</span>
    <div v-if="success">
      <h3>Employees ({{ count }})</h3>
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
  </div>
</template>

<script>
import Client from '../Client'

export default {
  name: 'EmployideesList',
  data () {
    return {
      loading: true,
      error: '',
      success: false,
      info: {},
      employees: [],
      count: 0
    }
  },
  async mounted () {
    const client = new Client('/employees')
    await client.fetch(this, 'info', ['employees', 'count'])
  }
}
</script>

<style>
</style>
