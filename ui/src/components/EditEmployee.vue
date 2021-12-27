<template>
<div>
  <span v-if="error">{{ error }}</span>
  <span v-if="loading">loading ...</span>
  <div v-if="employee">
    <h2>Edit Employee</h2>
    <p>
     Name: {{ employee.name }} <br />
     email: {{ employee.email }}
    </p>
    <ul>
      <li>
        <router-link
          :to="{name: 'EditBasic', params: { id }}"
        >
          Update basic info
        </router-link>
      </li>
      <li>
        <router-link
          :to="{name: 'EditAddress', params: { id }}"
          >
           Update address
        </router-link>
     </li>
    </ul>
  </div>
</div>
</template>

<script>
import Client from '../Client'

export default {
  name: 'EditEmployee',
  props: {
    id: String
  },
  data: function () {
    return {
      loading: true,
      error: '',
      success: false,
      status: '',
      employee: null
    }
  },
  mounted: async function () {
    const client = new Client(this)
    const json = await client.doRequest('/employee/' + this.id)
    if (!json) {
      return
    }
    this.employee = json.employee
  }
}
</script>

<style>
</style>
