<template>
  <div class="page-card">
    <div class="page-card-header">
      <span class="page-card-title">产品说明书管理</span>
      <el-button type="primary" @click="openDialog()">+ 添加说明书</el-button>
    </div>

    <el-table :data="manuals" v-loading="loading" stripe>
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="product_name" label="产品名称" min-width="200" />
      <el-table-column prop="description" label="描述" min-width="180" show-overflow-tooltip />
      <el-table-column label="文件" width="100">
        <template #default="{ row }">
          <el-link v-if="row.file_url" :href="row.file_url" target="_blank" type="primary" :underline="false">查看</el-link>
          <span v-else style="color:#aaa;font-size:12px">无</span>
        </template>
      </el-table-column>
      <el-table-column label="状态" width="80">
        <template #default="{ row }">
          <el-tag :type="row.is_active ? 'success' : 'info'" size="small">{{ row.is_active ? '启用' : '禁用' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="140" fixed="right">
        <template #default="{ row }">
          <el-button link type="primary" @click="openDialog(row)">编辑</el-button>
          <el-button link type="danger" @click="deleteItem(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- Dialog -->
    <el-dialog v-model="showDialog" :title="editId ? '编辑说明书' : '添加说明书'" width="560px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="产品名称"><el-input v-model="form.product_name" /></el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="PDF文件链接">
          <el-input v-model="form.file_url" placeholder="PDF文件URL" />
        </el-form-item>
        <el-form-item label="是否启用"><el-switch v-model="form.is_active" /></el-form-item>
        <el-form-item label="排序权重"><el-input-number v-model="form.sort_order" style="width:100%" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showDialog = false">取消</el-button>
        <el-button type="primary" @click="saveItem" :loading="saving">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { adminApi } from '@/api'
import { ElMessage, ElMessageBox } from 'element-plus'

const manuals = ref([])
const loading = ref(false)
const showDialog = ref(false)
const saving = ref(false)
const editId = ref(null)
const form = ref(defaultForm())

function defaultForm() {
  return { product_name: '', description: '', file_url: '', is_active: true, sort_order: 0 }
}

async function fetchManuals() {
  loading.value = true
  try {
    manuals.value = await adminApi.manuals()
  } finally {
    loading.value = false
  }
}

function openDialog(row = null) {
  editId.value = row?.id || null
  form.value = row ? { ...defaultForm(), ...row } : defaultForm()
  showDialog.value = true
}

async function saveItem() {
  if (!form.value.product_name) return ElMessage.warning('请填写产品名称')
  saving.value = true
  try {
    if (editId.value) {
      await adminApi.updateManual(editId.value, form.value)
    } else {
      await adminApi.createManual(form.value)
    }
    ElMessage.success('保存成功')
    showDialog.value = false
    await fetchManuals()
  } finally {
    saving.value = false
  }
}

async function deleteItem(id) {
  await ElMessageBox.confirm('确定删除？', '警告', { type: 'warning' })
  await adminApi.deleteManual(id)
  ElMessage.success('删除成功')
  await fetchManuals()
}

onMounted(fetchManuals)
</script>
