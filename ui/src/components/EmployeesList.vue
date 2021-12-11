<template>
  <div class="hello">
    <span v-if="loading">Loading ...</span>
    <div v-if="info">
        <p> {{ info.message }} </p>
    </div>
    <span v-if="error">{{ error }}</span>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  data () {
    return {
      loading: true,
      info: null,
      error: ''
    }
  },
  async mounted () {
    this.loading = true
    try {
      const response = await fetch('http://127.0.0.1:5678/api/hello')
      if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`)
      }
      const json = await response.json()
      this.info = json
      this.loading = false
      this.error = ''
    } catch (error) {
      this.loading = false
      this.error = error
    }
  }
}
</script>

<style>
</style>
