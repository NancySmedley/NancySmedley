import axios from 'axios'
import { ElMessage } from 'element-plus'

const api = axios.create({
  baseURL: '/api',
  timeout: 15000
})

api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

api.interceptors.response.use(
  res => res.data,
  err => {
    const msg = err.response?.data?.detail || '请求失败'
    if (err.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    } else {
      ElMessage.error(msg)
    }
    return Promise.reject(err)
  }
)

export default api

// Auth
export const authApi = {
  register: data => api.post('/users/register', data),
  login: data => api.post('/users/login', data),
  getMe: () => api.get('/users/me'),
  updateMe: data => api.put('/users/me', data),
  changePassword: data => api.put('/users/change-password', data),
}

// Products
export const productApi = {
  list: params => api.get('/products', { params }),
  detail: id => api.get(`/products/${id}`),
  categories: () => api.get('/products/category/all'),
  banners: () => api.get('/products/banners/all'),
}

// Cart
export const cartApi = {
  get: () => api.get('/cart'),
  add: data => api.post('/cart', data),
  update: (id, data) => api.put(`/cart/${id}`, data),
  remove: id => api.delete(`/cart/${id}`),
  clear: () => api.delete('/cart'),
}

// Orders
export const orderApi = {
  create: data => api.post('/orders', data),
  list: params => api.get('/orders', { params }),
  detail: id => api.get(`/orders/${id}`),
  cancel: id => api.put(`/orders/${id}/cancel`),
}

// Addresses
export const addressApi = {
  list: () => api.get('/users/addresses'),
  create: data => api.post('/users/addresses', data),
  update: (id, data) => api.put(`/users/addresses/${id}`, data),
  remove: id => api.delete(`/users/addresses/${id}`),
}

// Admin
export const adminApi = {
  stats: () => api.get('/admin/stats'),
  upload: file => {
    const form = new FormData()
    form.append('file', file)
    return api.post('/admin/upload', form, { headers: { 'Content-Type': 'multipart/form-data' } })
  },
  // products
  products: params => api.get('/admin/products', { params }),
  createProduct: data => api.post('/admin/products', data),
  updateProduct: (id, data) => api.put(`/admin/products/${id}`, data),
  deleteProduct: id => api.delete(`/admin/products/${id}`),
  // categories
  categories: () => api.get('/admin/categories'),
  createCategory: data => api.post('/admin/categories', data),
  updateCategory: (id, data) => api.put(`/admin/categories/${id}`, data),
  deleteCategory: id => api.delete(`/admin/categories/${id}`),
  // orders
  orders: params => api.get('/admin/orders', { params }),
  updateOrderStatus: (id, data) => api.put(`/admin/orders/${id}/status`, data),
  // users
  users: params => api.get('/admin/users', { params }),
  toggleUser: (id, data) => api.put(`/admin/users/${id}/status`, data),
  // banners
  banners: () => api.get('/admin/banners'),
  createBanner: data => api.post('/admin/banners', data),
  updateBanner: (id, data) => api.put(`/admin/banners/${id}`, data),
  deleteBanner: id => api.delete(`/admin/banners/${id}`),
}
