import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', component: () => import('@/views/Home.vue') },
  { path: '/ai-headphones', component: () => import('@/views/AiHeadphones.vue') },
  { path: '/brand', component: () => import('@/views/Brand.vue') },
  { path: '/download', component: () => import('@/views/Download.vue') },
  { path: '/manual', component: () => import('@/views/Manual.vue') },
  { path: '/cooperation', component: () => import('@/views/Cooperation.vue') },
  { path: '/about', component: () => import('@/views/About.vue') },
  { path: '/:pathMatch(.*)*', redirect: '/' }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 })
})

export default router
