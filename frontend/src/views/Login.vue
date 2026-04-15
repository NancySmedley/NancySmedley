<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-logo">i<span>K</span>F</div>
      <p class="auth-subtitle">欢迎回来，请登录您的账号</p>

      <el-form :model="form" label-position="top" @submit.prevent="handleLogin">
        <el-form-item label="用户名">
          <el-input v-model="form.username" placeholder="请输入用户名" size="large" prefix-icon="User" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input
            v-model="form.password" type="password" placeholder="请输入密码"
            size="large" prefix-icon="Lock" show-password
          />
        </el-form-item>
        <el-button
          type="primary" native-type="submit" size="large"
          style="width:100%;margin-top:8px" :loading="loading"
        >登录</el-button>
      </el-form>

      <div style="text-align:center;margin-top:20px;font-size:14px;color:#666">
        还没有账号？
        <router-link to="/register" style="color:var(--accent);font-weight:500">立即注册</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/store/user'
import { useCartStore } from '@/store/cart'
import { ElMessage } from 'element-plus'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const cartStore = useCartStore()

const form = ref({ username: '', password: '' })
const loading = ref(false)

async function handleLogin() {
  if (!form.value.username || !form.value.password) {
    return ElMessage.warning('请填写用户名和密码')
  }
  loading.value = true
  try {
    await userStore.login(form.value)
    await cartStore.fetchCart()
    ElMessage.success('登录成功！')
    const redirect = route.query.redirect || '/'
    router.push(redirect)
  } finally {
    loading.value = false
  }
}
</script>
