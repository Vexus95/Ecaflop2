<template>
<div>
  <EmployeeForm
    ref="form"
    v-if="initialData"
    :initialData="initialData"
    :onSubmit="this.onSubmit"
    submitText="Save"
  />
  <span>{{ status }}</span>
</div>
</template>

<script>
import EmployeeForm from './EmployeeForm.vue'
import Client from '../Client'

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
      initialData: null
    }
  },
  mounted: async function () {
    const client = new Client(this)
    const json = await client.doRequest(this.url())
    this.initialData = json.employee
  },
  methods: {
    url: function () {
      return '/employee/' + this.id
    },
    onSubmit: async function (payload) {
      this.status = 'Saving ...'
      console.log('payload', payload)
      const client = new Client(this)
      const json = await client.doRequest(
        this.url(),
        { method: 'PUT', body: JSON.stringify(payload) }
      )
      if (!json) {
        this.status = ''
        return
      }
      this.status = 'Saved'
    }
  }
}
</script>

<style>
</style>
