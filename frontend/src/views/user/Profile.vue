<template>
  <div style="background:white;border-radius:12px;padding:28px;box-shadow:var(--shadow)">
    <h3 style="font-size:18px;font-weight:600;margin-bottom:24px">个人信息</h3>
    <el-form :model="form" label-width="80px" style="max-width:420px">
      <el-form-item label="用户名">
        <el-input :value="userStore.user?.username" disabled />
      </el-form-item>
      <el-form-item label="邮箱">
        <el-input :value="userStore.user?.email" disabled />
      </el-form-item>
      <el-form-item label="手机号">
        <el-input v-model="form.phone" placeholder="请输入手机号" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="saveProfile" :loading="saving">保存修改</el-button>
      </el-form-item>
    </el-form>

    <el-divider />

    <h3 style="font-size:16px;font-weight:600;margin-bottom:20px">修改密码</h3>
    <el-form :model="pwdForm" label-width="80px" style="max-width:420px">
      <el-form-item label="原密码">
        <el-input v-model="pwdForm.old_password" type="password" show-password />
      </el-form-item>
      <el-form-item label="新密码">
        <el-input v-model="pwdForm.new_password" type="password" show-password />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="changePwd" :loading="changingPwd">修改密码</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/store/user'
import { authApi } from '@/api'
import { ElMessage } from 'element-plus'

const userStore = useUserStore()
const form = ref({ phone: userStore.user?.phone || '' })
const pwdForm = ref({ old_password: '', new_password: '' })
const saving = ref(false)
const changingPwd = ref(false)

async function saveProfile() {
  saving.value = true
  try {
    await authApi.updateMe(form.value)
    await userStore.fetchMe()
    ElMessage.success('保存成功')
  } finally {
    saving.value = false
  }
}

async function changePwd() {
  if (!pwdForm.value.old_password || !pwdForm.value.new_password) return ElMessage.warning('请填写完整')
  changingPwd.value = true
  try {
    await authApi.changePassword(pwdForm.value)
    ElMessage.success('密码修改成功，请重新登录')
    pwdForm.value = { old_password: '', new_password: '' }
  } finally {
    changingPwd.value = false
  }
}
</script>
