<template>
  <div class="page-card">
    <div class="page-card-header">
      <span class="page-card-title">页面内容管理</span>
    </div>

    <div style="margin-bottom:16px;color:#666;font-size:13px">
      管理品牌文化、品牌合作、关于我们等静态页面的内容（如果不填则展示默认内容）
    </div>

    <el-tabs v-model="activeTab">
      <el-tab-pane label="品牌文化" name="brand" />
      <el-tab-pane label="品牌合作" name="cooperation" />
      <el-tab-pane label="关于我们" name="about" />
    </el-tabs>

    <div v-loading="loading" style="margin-top:20px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="页面标题">
          <el-input v-model="form.title" placeholder="页面大标题" />
        </el-form-item>
        <el-form-item label="顶部横幅图">
          <div style="display:flex;gap:10px;align-items:center">
            <el-input v-model="bannerImg" placeholder="顶部横幅图片URL" style="flex:1" />
            <el-upload :show-file-list="false" :before-upload="uploadBanner">
              <el-button>上传</el-button>
            </el-upload>
          </div>
          <el-image v-if="bannerImg" :src="bannerImg" style="height:100px;margin-top:8px;border-radius:4px;object-fit:cover" />
        </el-form-item>
        <el-form-item label="页面内容">
          <el-input
            v-model="form.content"
            type="textarea"
            :rows="14"
            placeholder="支持HTML格式内容，如 <h2>标题</h2><p>段落文字</p>"
          />
        </el-form-item>
      </el-form>
      <div style="display:flex;justify-content:flex-end;margin-top:16px">
        <el-button type="primary" @click="savePage" :loading="saving">保存</el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed, onMounted } from 'vue'
import { adminApi } from '@/api'
import { ElMessage } from 'element-plus'

const activeTab = ref('brand')
const loading = ref(false)
const saving = ref(false)
const pagesCache = ref({})
const form = ref({ title: '', content: '', images: '[]' })

const bannerImg = computed({
  get() {
    try { return JSON.parse(form.value.images || '[]')[0] || '' } catch { return '' }
  },
  set(v) {
    form.value.images = JSON.stringify(v ? [v] : [])
  }
})

async function loadPage(key) {
  if (pagesCache.value[key]) {
    form.value = { ...pagesCache.value[key] }
    return
  }
  loading.value = true
  try {
    const data = await adminApi.pages()
    const found = data.find(p => p.page_key === key)
    if (found) {
      pagesCache.value[key] = found
      form.value = { ...found }
    } else {
      form.value = { title: '', content: '', images: '[]' }
    }
  } catch {
    form.value = { title: '', content: '', images: '[]' }
  } finally {
    loading.value = false
  }
}

async function uploadBanner(file) {
  const res = await adminApi.upload(file)
  bannerImg.value = res.url
  return false
}

async function savePage() {
  saving.value = true
  try {
    await adminApi.upsertPage(activeTab.value, form.value)
    pagesCache.value[activeTab.value] = { ...form.value, page_key: activeTab.value }
    ElMessage.success('保存成功')
  } finally {
    saving.value = false
  }
}

watch(activeTab, (key) => loadPage(key))
onMounted(() => loadPage(activeTab.value))
</script>
