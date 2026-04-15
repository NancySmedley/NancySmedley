<template>
  <div class="page-card">
    <div class="page-card-header">
      <span class="page-card-title">分类管理</span>
      <el-button type="primary" @click="openDialog()">+ 添加分类</el-button>
    </div>

    <el-table :data="categories" v-loading="loading" stripe>
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="icon" label="图标" width="60" />
      <el-table-column prop="name" label="分类名称" />
      <el-table-column prop="description" label="描述" show-overflow-tooltip />
      <el-table-column prop="sort_order" label="排序" width="80" />
      <el-table-column label="状态" width="80">
        <template #default="{ row }">
          <el-tag :type="row.is_active ? 'success' : 'info'" size="small">{{ row.is_active ? '启用' : '禁用' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="140">
        <template #default="{ row }">
          <el-button link type="primary" @click="openDialog(row)">编辑</el-button>
          <el-button link type="danger" @click="deleteCategory(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="showDialog" :title="editId ? '编辑分类' : '添加分类'" width="440px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="分类名称"><el-input v-model="form.name" /></el-form-item>
        <el-form-item label="图标"><el-input v-model="form.icon" placeholder="如：🎧" /></el-form-item>
        <el-form-item label="描述"><el-input v-model="form.description" type="textarea" /></el-form-item>
        <el-form-item label="排序权重"><el-input-number v-model="form.sort_order" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showDialog = false">取消</el-button>
        <el-button type="primary" @click="save" :loading="saving">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { adminApi } from '@/api'
import { ElMessage, ElMessageBox } from 'element-plus'

const categories = ref([])
const loading = ref(false)
const showDialog = ref(false)
const saving = ref(false)
const editId = ref(null)
const form = ref({ name: '', icon: '', description: '', sort_order: 0 })

async function fetchCategories() {
  loading.value = true
  categories.value = await adminApi.categories()
  loading.value = false
}

function openDialog(row = null) {
  editId.value = row?.id || null
  form.value = row ? { name: row.name, icon: row.icon, description: row.description, sort_order: row.sort_order } : { name: '', icon: '', description: '', sort_order: 0 }
  showDialog.value = true
}

async function save() {
  if (!form.value.name) return ElMessage.warning('请填写分类名称')
  saving.value = true
  try {
    if (editId.value) {
      await adminApi.updateCategory(editId.value, form.value)
    } else {
      await adminApi.createCategory(form.value)
    }
    ElMessage.success('保存成功')
    showDialog.value = false
    await fetchCategories()
  } finally {
    saving.value = false
  }
}

async function deleteCategory(id) {
  await ElMessageBox.confirm('确定删除此分类？', '警告', { type: 'warning' })
  await adminApi.deleteCategory(id)
  ElMessage.success('删除成功')
  await fetchCategories()
}

onMounted(fetchCategories)
</script>
