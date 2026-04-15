import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/store/user'

const routes = [
  { path: '/', component: () => import('@/views/Home.vue') },
  { path: '/products', component: () => import('@/views/Products.vue') },
  { path: '/products/:id', component: () => import('@/views/ProductDetail.vue') },
  { path: '/cart', component: () => import('@/views/Cart.vue'), meta: { requiresAuth: true } },
  { path: '/checkout', component: () => import('@/views/Checkout.vue'), meta: { requiresAuth: true } },
  { path: '/login', component: () => import('@/views/Login.vue') },
  { path: '/register', component: () => import('@/views/Register.vue') },
  {
    path: '/user',
    component: () => import('@/views/UserCenter.vue'),
    meta: { requiresAuth: true },
    children: [
      { path: '', redirect: '/user/profile' },
      { path: 'profile', component: () => import('@/views/user/Profile.vue') },
      { path: 'orders', component: () => import('@/views/user/Orders.vue') },
      { path: 'addresses', component: () => import('@/views/user/Addresses.vue') },
    ]
  },
  { path: '/:pathMatch(.*)*', redirect: '/' }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 })
})

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    next({ path: '/login', query: { redirect: to.fullPath } })
  } else {
    next()
  }
})

export default router
