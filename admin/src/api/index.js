import axios from 'axios'
import { ElMessage } from 'element-plus'

const api = axios.create({ baseURL: '/api', timeout: 15000 })

api.interceptors.request.use(cfg => {
  const token = localStorage.getItem('admin_token')
  if (token) cfg.headers.Authorization = `Bearer ${token}`
  return cfg
})

api.interceptors.response.use(
  res => res.data,
  err => {
    const msg = err.response?.data?.detail || '请求失败'
    if (err.response?.status === 401) {
      localStorage.removeItem('admin_token')
      localStorage.removeItem('admin_user')
      window.location.href = '/admin/login'
    } else {
      ElMessage.error(msg)
    }
    return Promise.reject(err)
  }
)

export default api
export const adminApi = {
  login: d => api.post('/users/login', d),
  stats: () => api.get('/admin/stats'),
  upload: file => {
    const form = new FormData()
    form.append('file', file)
    return api.post('/admin/upload', form)
  },
  products: p => api.get('/admin/products', { params: p }),
  createProduct: d => api.post('/admin/products', d),
  updateProduct: (id, d) => api.put(`/admin/products/${id}`, d),
  deleteProduct: id => api.delete(`/admin/products/${id}`),
  categories: () => api.get('/admin/categories'),
  createCategory: d => api.post('/admin/categories', d),
  updateCategory: (id, d) => api.put(`/admin/categories/${id}`, d),
  deleteCategory: id => api.delete(`/admin/categories/${id}`),
  orders: p => api.get('/admin/orders', { params: p }),
  updateOrderStatus: (id, d) => api.put(`/admin/orders/${id}/status`, d),
  users: p => api.get('/admin/users', { params: p }),
  toggleUser: (id, d) => api.put(`/admin/users/${id}/status`, d),
  banners: () => api.get('/admin/banners'),
  createBanner: d => api.post('/admin/banners', d),
  updateBanner: (id, d) => api.put(`/admin/banners/${id}`, d),
  deleteBanner: id => api.delete(`/admin/banners/${id}`),
}
