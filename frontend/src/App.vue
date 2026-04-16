<template>
  <AppNavbar />
  <main class="page-wrap">
    <router-view />
  </main>
  <AppFooter />
</template>

<script setup>
import AppNavbar from '@/components/AppNavbar.vue'
import AppFooter from '@/components/AppFooter.vue'
</script>
