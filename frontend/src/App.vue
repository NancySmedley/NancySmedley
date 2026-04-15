<template>
  <router-view v-if="isAuthPage" />
  <template v-else>
    <AppNavbar />
    <main class="page-wrap">
      <router-view />
    </main>
    <AppFooter />
  </template>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '@/store/user'
import { useCartStore } from '@/store/cart'
import AppNavbar from '@/components/AppNavbar.vue'
import AppFooter from '@/components/AppFooter.vue'

const route = useRoute()
const userStore = useUserStore()
const cartStore = useCartStore()

const isAuthPage = computed(() => ['/login', '/register'].includes(route.path))

if (userStore.isLoggedIn) {
  cartStore.fetchCart()
  userStore.fetchMe()
}
</script>
