<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-logo">i<span>K</span>F</div>
      <p class="auth-subtitle">创建账号，开始音乐之旅</p>

      <el-form :model="form" label-position="top" @submit.prevent="handleRegister">
        <el-form-item label="用户名">
          <el-input v-model="form.username" placeholder="请输入用户名（4-20位）" size="large" prefix-icon="User" />
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="form.email" placeholder="请输入邮箱" size="large" prefix-icon="Message" />
        </el-form-item>
        <el-form-item label="手机号（选填）">
          <el-input v-model="form.phone" placeholder="请输入手机号" size="large" prefix-icon="Phone" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input
            v-model="form.password" type="password"
            placeholder="请输入密码（至少6位）" size="large" prefix-icon="Lock" show-password
          />
        </el-form-item>
        <el-button
          type="primary" native-type="submit" size="large"
          style="width:100%;margin-top:8px" :loading="loading"
        >注册</el-button>
      </el-form>

      <div style="text-align:center;margin-top:20px;font-size:14px;color:#666">
        已有账号？
        <router-link to="/login" style="color:var(--accent);font-weight:500">立即登录</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'
import { useCartStore } from '@/store/cart'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()
const cartStore = useCartStore()

const form = ref({ username: '', email: '', phone: '', password: '' })
const loading = ref(false)

async function handleRegister() {
  if (!form.value.username || !form.value.email || !form.value.password) {
    return ElMessage.warning('请填写必填项')
  }
  if (form.value.password.length < 6) {
    return ElMessage.warning('密码至少6位')
  }
  loading.value = true
  try {
    await userStore.register(form.value)
    await cartStore.fetchCart()
    ElMessage.success('注册成功！')
    router.push('/')
  } finally {
    loading.value = false
  }
}
</script>
