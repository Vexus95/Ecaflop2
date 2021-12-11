<template>
  <div class="hello">
    <h1>{{ info.message }}</h1>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  data () {
    return {
      info: null
    }
  },
  async mounted () {
    console.log('hello')
    const response = await fetch('http://127.0.0.1:5678/api/hello')
    console.log(response)
    const json = await response.json()
    this.info = json
  }
}
</script>

<style>
</style>
