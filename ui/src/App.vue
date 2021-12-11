<template>
  <div id="app">
    <h1 id='title'>HR Manager</h1>
    <ul>
      <li><router-link to="/employees">List Employees</router-link></li>
      <li><router-link to="/reset-db">Reset database</router-link></li>
    </ul>
    <router-view/>
  </div>
</template>

<style>
body {
  margin: 5% auto;
  max-width: 73%;
}
</style>
