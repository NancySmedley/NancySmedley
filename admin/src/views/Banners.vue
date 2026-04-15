<template>
  <div class="page-card">
    <div class="page-card-header">
      <span class="page-card-title">轮播图管理</span>
      <el-button type="primary" @click="openDialog()">+ 添加轮播图</el-button>
    </div>

    <el-table :data="banners" v-loading="loading" stripe>
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column label="图片" width="160">
        <template #default="{ row }">
          <el-image :src="row.image" style="width:140px;height:50px;border-radius:4px;object-fit:cover" />
        </template>
      </el-table-column>
      <el-table-column prop="title" label="标题" />
      <el-table-column prop="link" label="链接" show-overflow-tooltip />
      <el-table-column prop="sort_order" label="排序" width="80" />
      <el-table-column label="状态" width="80">
        <template #default="{ row }">
          <el-tag :type="row.is_active ? 'success' : 'info'" size="small">{{ row.is_active ? '显示' : '隐藏' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="140">
        <template #default="{ row }">
          <el-button link type="primary" @click="openDialog(row)">编辑</el-button>
          <el-button link type="danger" @click="deleteBanner(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="showDialog" :title="editId ? '编辑轮播图' : '添加轮播图'" width="500px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="标题"><el-input v-model="form.title" /></el-form-item>
        <el-form-item label="图片">
          <div style="display:flex;gap:12px;align-items:center">
            <el-input v-model="form.image" placeholder="图片URL" style="flex:1" />
            <el-upload :show-file-list="false" :before-upload="uploadImg">
              <el-button>上传</el-button>
            </el-upload>
          </div>
          <el-image v-if="form.image" :src="form.image" style="width:100%;height:80px;border-radius:6px;margin-top:8px;object-fit:cover" />
        </el-form-item>
        <el-form-item label="链接"><el-input v-model="form.link" placeholder="/products" /></el-form-item>
        <el-form-item label="排序"><el-input-number v-model="form.sort_order" /></el-form-item>
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

const banners = ref([])
const loading = ref(false)
const showDialog = ref(false)
const saving = ref(false)
const editId = ref(null)
const form = ref({ title: '', image: '', link: '', sort_order: 0 })

async function fetchBanners() {
  loading.value = true
  banners.value = await adminApi.banners()
  loading.value = false
}

async function uploadImg(file) {
  const res = await adminApi.upload(file)
  form.value.image = res.url
  return false
}

function openDialog(row = null) {
  editId.value = row?.id || null
  form.value = row ? { title: row.title, image: row.image, link: row.link, sort_order: row.sort_order } : { title: '', image: '', link: '', sort_order: 0 }
  showDialog.value = true
}

async function save() {
  if (!form.value.image) return ElMessage.warning('请上传或填写图片地址')
  saving.value = true
  try {
    if (editId.value) {
      await adminApi.updateBanner(editId.value, form.value)
    } else {
      await adminApi.createBanner(form.value)
    }
    ElMessage.success('保存成功')
    showDialog.value = false
    await fetchBanners()
  } finally {
    saving.value = false
  }
}

async function deleteBanner(id) {
  await ElMessageBox.confirm('确定删除此轮播图？', '警告', { type: 'warning' })
  await adminApi.deleteBanner(id)
  ElMessage.success('删除成功')
  await fetchBanners()
}

onMounted(fetchBanners)
</script>
