<template>
  <div class="employees-list">
    <span v-if="loading">Loading ...</span>
    <span v-if="error">{{ error }}</span>
    <div v-if="info">
      <h3>Employees ({{ info.count }})</h3>
      <table class="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>email</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="employee in info.employees" :key="employee.id">
            <td>
               <router-link
                 to="/employee/{{ employee.id }}"
                >
                {{ employee.id }}
                </rooter-link>
            </td>
            <td>{{ employee.name }}</td>
            <td>{{ employee.email }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
