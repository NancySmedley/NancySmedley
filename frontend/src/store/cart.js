import { defineStore } from 'pinia'
import { cartApi } from '@/api'
import { ElMessage } from 'element-plus'

export const useCartStore = defineStore('cart', {
  state: () => ({
    items: [],
    loading: false,
  }),
  getters: {
    count: state => state.items.reduce((sum, i) => sum + i.quantity, 0),
    total: state => state.items.reduce((sum, i) => sum + i.product.price * i.quantity, 0),
    selectedItems: state => state.items.filter(i => i.selected),
    selectedTotal: state => state.items
      .filter(i => i.selected)
      .reduce((sum, i) => sum + i.product.price * i.quantity, 0),
  },
  actions: {
    async fetchCart() {
      try {
        this.loading = true
        const items = await cartApi.get()
        this.items = items.map(i => ({ ...i, selected: true }))
      } catch {
        // not logged in
      } finally {
        this.loading = false
      }
    },
    async addToCart(productId, quantity = 1) {
      await cartApi.add({ product_id: productId, quantity })
      ElMessage.success('已加入购物车')
      await this.fetchCart()
    },
    async updateQuantity(itemId, quantity) {
      await cartApi.update(itemId, { quantity })
      await this.fetchCart()
    },
    async removeItem(itemId) {
      await cartApi.remove(itemId)
      await this.fetchCart()
    },
    async clearCart() {
      await cartApi.clear()
      this.items = []
    },
    toggleSelect(itemId) {
      const item = this.items.find(i => i.id === itemId)
      if (item) item.selected = !item.selected
    },
    toggleSelectAll(val) {
      this.items.forEach(i => i.selected = val)
    }
  }
})
