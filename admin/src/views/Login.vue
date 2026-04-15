<template>
  <div class="admin-login">
    <div class="login-box">
      <div class="login-logo">i<span>K</span>F</div>
      <p class="login-sub">后台管理系统</p>
      <el-form :model="form" @submit.prevent="handleLogin" label-position="top">
        <el-form-item label="管理员账号">
          <el-input v-model="form.username" placeholder="请输入账号" size="large" prefix-icon="User" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.password" type="password" placeholder="请输入密码" size="large" prefix-icon="Lock" show-password />
        </el-form-item>
        <el-button type="primary" native-type="submit" size="large" style="width:100%;margin-top:8px" :loading="loading">
          登录
        </el-button>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAdminStore } from '@/store/admin'
import { ElMessage } from 'element-plus'

const router = useRouter()
const adminStore = useAdminStore()
const form = ref({ username: 'admin', password: 'admin123456' })
const loading = ref(false)

async function handleLogin() {
  loading.value = true
  try {
    await adminStore.login(form.value)
    ElMessage.success('登录成功')
    router.push('/admin/dashboard')
  } finally {
    loading.value = false
  }
}
</script>
