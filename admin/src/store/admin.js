import { defineStore } from 'pinia'
import { adminApi } from '@/api'

export const useAdminStore = defineStore('admin', {
  state: () => ({
    token: localStorage.getItem('admin_token') || null,
    user: JSON.parse(localStorage.getItem('admin_user') || 'null'),
  }),
  getters: {
    isLoggedIn: s => !!s.token,
  },
  actions: {
    async login(creds) {
      const res = await adminApi.login(creds)
      if (res.user.role !== 'admin') throw new Error('无管理员权限')
      this.token = res.access_token
      this.user = res.user
      localStorage.setItem('admin_token', res.access_token)
      localStorage.setItem('admin_user', JSON.stringify(res.user))
      return res
    },
    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('admin_token')
      localStorage.removeItem('admin_user')
    }
  }
})
