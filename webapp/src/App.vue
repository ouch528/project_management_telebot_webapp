<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
      <nav>
        <RouterLink to="/"></RouterLink>
        <RouterLink to="/test">Test</RouterLink>
      </nav>
      <RouterView />
  </header>
</template>

<style scoped>

</style>
