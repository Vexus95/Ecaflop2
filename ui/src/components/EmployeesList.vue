<template>
  <div class="employees-list">
    <span v-if="loading">Loading ...</span>
    <span v-if="error">{{ error }}</span>
    <div v-if="success">
      <h3>Employees ({{ employees.length }})</h3>
      <table class="table">
        <thead>
          <tr>
            <th>Name</th>
            <th>email</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="employee in employees" :key="employee.id">
            <td>{{ employee.name }}</td>
            <td>{{ employee.email }}</td>
            <td>
              <router-link :to="`employee/${employee.id}`"
                 class='btn btn-primary'
               >
               Edit
             </router-link>
          </td>
            <td>
              <router-link :to="`employee/${employee.id}/delete`"
                 class='btn btn-danger'
               >
               Delete
             </router-link>
          </td>
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
  methods: {
    onDelete: async function (id) {
      this.$router.push('/employee/' + id + '/delete')
    },
    onEdit: function (employee) {
      this.$router.push('/employee/' + employee.id)
    },
    refresh: async function () {
      const client = new Client(this)
      const json = await client.doRequest('/employees')
      if (!json) {
        return
      }
      this.employees = json
    }
  },
  async mounted () {
    this.refresh()
  }
}
</script>

<style>
</style>
