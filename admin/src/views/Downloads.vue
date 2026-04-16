<template>
  <div class="page-card">
    <div class="page-card-header">
      <span class="page-card-title">软件下载管理</span>
      <el-button type="primary" @click="openDialog()">+ 添加软件</el-button>
    </div>

    <el-table :data="downloads" v-loading="loading" stripe>
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column label="图标" width="70">
        <template #default="{ row }">
          <el-image v-if="row.cover_image" :src="row.cover_image" style="width:44px;height:44px;border-radius:10px;object-fit:cover" />
          <span v-else style="color:#aaa;font-size:12px">无</span>
        </template>
      </el-table-column>
      <el-table-column prop="name" label="软件名称" min-width="160" />
      <el-table-column prop="version" label="版本" width="100" />
      <el-table-column label="下载链接" min-width="200">
        <template #default="{ row }">
          <div style="font-size:12px;color:#666">
            <div v-if="row.ios_url">iOS ✓</div>
            <div v-if="row.android_url">Android ✓</div>
            <div v-if="row.windows_url">Windows ✓</div>
            <div v-if="row.mac_url">macOS ✓</div>
          </div>
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
    <el-dialog v-model="showDialog" :title="editId ? '编辑软件' : '添加软件'" width="600px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="软件名称"><el-input v-model="form.name" /></el-form-item>
        <el-form-item label="版本号"><el-input v-model="form.version" placeholder="如：v3.2.1" /></el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" :rows="3" />
        </el-form-item>
        <el-form-item label="图标URL">
          <div style="display:flex;gap:10px;align-items:center">
            <el-input v-model="form.cover_image" placeholder="图标图片URL" style="flex:1" />
            <el-upload :show-file-list="false" :before-upload="f => uploadImg(f, 'cover_image')">
              <el-button>上传</el-button>
            </el-upload>
          </div>
        </el-form-item>
        <el-form-item label="iOS下载链接"><el-input v-model="form.ios_url" placeholder="App Store链接" /></el-form-item>
        <el-form-item label="Android下载链接"><el-input v-model="form.android_url" placeholder="APK或应用商店链接" /></el-form-item>
        <el-form-item label="Windows下载链接"><el-input v-model="form.windows_url" placeholder=".exe安装包链接" /></el-form-item>
        <el-form-item label="macOS下载链接"><el-input v-model="form.mac_url" placeholder=".dmg安装包链接" /></el-form-item>
        <el-form-item label="是否启用"><el-switch v-model="form.is_active" /></el-form-item>
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

const downloads = ref([])
const loading = ref(false)
const showDialog = ref(false)
const saving = ref(false)
const editId = ref(null)
const form = ref(defaultForm())

function defaultForm() {
  return {
    name: '', version: '', description: '', cover_image: '',
    ios_url: '', android_url: '', windows_url: '', mac_url: '',
    is_active: true, sort_order: 0
  }
}

async function fetchDownloads() {
  loading.value = true
  try {
    downloads.value = await adminApi.downloads()
  } finally {
    loading.value = false
  }
}

async function uploadImg(file, field) {
  const res = await adminApi.upload(file)
  form.value[field] = res.url
  return false
}

function openDialog(row = null) {
  editId.value = row?.id || null
  form.value = row ? { ...defaultForm(), ...row } : defaultForm()
  showDialog.value = true
}

async function saveItem() {
  if (!form.value.name) return ElMessage.warning('请填写软件名称')
  saving.value = true
  try {
    if (editId.value) {
      await adminApi.updateDownload(editId.value, form.value)
    } else {
      await adminApi.createDownload(form.value)
    }
    ElMessage.success('保存成功')
    showDialog.value = false
    await fetchDownloads()
  } finally {
    saving.value = false
  }
}

async function deleteItem(id) {
  await ElMessageBox.confirm('确定删除？', '警告', { type: 'warning' })
  await adminApi.deleteDownload(id)
  ElMessage.success('删除成功')
  await fetchDownloads()
}

onMounted(fetchDownloads)
</script>
