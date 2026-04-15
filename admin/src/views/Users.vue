<template>
  <div class="page-card">
    <div class="page-card-header">
      <span class="page-card-title">用户管理</span>
    </div>

    <div style="display:flex;gap:12px;margin-bottom:16px">
      <el-input v-model="keyword" placeholder="搜索用户名/邮箱" style="width:260px" clearable @change="fetchUsers" />
      <el-button @click="fetchUsers">搜索</el-button>
    </div>

    <el-table :data="users" v-loading="loading" stripe>
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="username" label="用户名" width="120" />
      <el-table-column prop="email" label="邮箱" width="200" />
      <el-table-column prop="phone" label="手机号" width="140" />
      <el-table-column label="状态" width="90">
        <template #default="{ row }">
          <el-tag :type="row.is_active ? 'success' : 'danger'" size="small">
            {{ row.is_active ? '正常' : '禁用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="注册时间" width="170">
        <template #default="{ row }">{{ new Date(row.created_at).toLocaleString('zh-CN') }}</template>
      </el-table-column>
      <el-table-column label="操作" width="120">
        <template #default="{ row }">
          <el-button
            link :type="row.is_active ? 'danger' : 'success'"
            @click="toggleUser(row)"
          >{{ row.is_active ? '禁用' : '启用' }}</el-button>
        </template>
      </el-table-column>
    </el-table>

    <div style="margin-top:16px;text-align:right">
      <el-pagination background layout="total, prev, pager, next"
        :total="total" :page-size="pageSize"
        v-model:current-page="page" @current-change="fetchUsers"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { adminApi } from '@/api'
import { ElMessage } from 'element-plus'

const users = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = 20
const loading = ref(false)
const keyword = ref('')

async function fetchUsers() {
  loading.value = true
  try {
    const params = { page: page.value, page_size: pageSize }
    if (keyword.value) params.keyword = keyword.value
    const res = await adminApi.users(params)
    users.value = res.items
    total.value = res.total
  } finally {
    loading.value = false
  }
}

async function toggleUser(user) {
  await adminApi.toggleUser(user.id, { is_active: !user.is_active })
  ElMessage.success(user.is_active ? '已禁用用户' : '已启用用户')
  await fetchUsers()
}

onMounted(fetchUsers)
</script>
