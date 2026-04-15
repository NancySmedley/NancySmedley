import { defineStore } from 'pinia'
import { authApi } from '@/api'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: JSON.parse(localStorage.getItem('user') || 'null'),
  }),
  getters: {
    isLoggedIn: state => !!state.token,
    isAdmin: state => state.user?.role === 'admin',
  },
  actions: {
    async login(credentials) {
      const res = await authApi.login(credentials)
      this.token = res.access_token
      this.user = res.user
      localStorage.setItem('token', res.access_token)
      localStorage.setItem('user', JSON.stringify(res.user))
      return res
    },
    async register(data) {
      const res = await authApi.register(data)
      this.token = res.access_token
      this.user = res.user
      localStorage.setItem('token', res.access_token)
      localStorage.setItem('user', JSON.stringify(res.user))
      return res
    },
    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    },
    async fetchMe() {
      if (!this.token) return
      try {
        const user = await authApi.getMe()
        this.user = user
        localStorage.setItem('user', JSON.stringify(user))
      } catch {
        this.logout()
      }
    }
  }
})
