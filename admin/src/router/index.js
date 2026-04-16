import { createRouter, createWebHistory } from 'vue-router'
import { useAdminStore } from '@/store/admin'

const routes = [
  { path: '/admin/login', component: () => import('@/views/Login.vue') },
  {
    path: '/admin',
    component: () => import('@/views/Layout.vue'),
    meta: { requiresAuth: true },
    children: [
      { path: '', redirect: '/admin/dashboard' },
      { path: 'dashboard', component: () => import('@/views/Dashboard.vue') },
      { path: 'products', component: () => import('@/views/Products.vue') },
      { path: 'categories', component: () => import('@/views/Categories.vue') },
      { path: 'banners', component: () => import('@/views/Banners.vue') },
      { path: 'downloads', component: () => import('@/views/Downloads.vue') },
      { path: 'manuals', component: () => import('@/views/Manuals.vue') },
      { path: 'pages', component: () => import('@/views/Pages.vue') },
      { path: 'users', component: () => import('@/views/Users.vue') },
    ]
  },
  { path: '/:pathMatch(.*)*', redirect: '/admin' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const store = useAdminStore()
  if (to.meta.requiresAuth && !store.isLoggedIn) {
    next('/admin/login')
  } else {
    next()
  }
})

export default router
