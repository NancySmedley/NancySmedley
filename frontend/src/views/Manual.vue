<template>
  <div class="static-page">
    <img
      src="https://picsum.photos/seed/shinesphere-manual/1400/300"
      alt="产品说明书"
      class="products-banner"
    />
    <div class="container static-content">
      <h1 class="static-title">产品说明书</h1>
      <div v-if="loading" style="text-align:center;padding:60px 0;color:#999">加载中...</div>
      <div v-else-if="!manuals.length" style="text-align:center;padding:60px 0;color:#999">暂无说明书</div>
      <div v-else class="manual-grid">
        <div v-for="m in manuals" :key="m.id" class="manual-card">
          <div class="manual-icon">📄</div>
          <div class="manual-name">{{ m.product_name }}</div>
          <div class="manual-desc" v-if="m.description">{{ m.description }}</div>
          <a
            v-if="m.file_url"
            :href="m.file_url"
            target="_blank"
            class="manual-download-btn"
          >下载说明书</a>
          <span v-else class="manual-unavailable">暂无文件</span>
        </div>
      </div>
    </div>
    <div class="scroll-top" @click="scrollTop">↑</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { productApi } from '@/api'

const manuals = ref([])
const loading = ref(false)

function scrollTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

onMounted(async () => {
  loading.value = true
  try {
    manuals.value = await productApi.manuals()
  } catch {
    manuals.value = []
  } finally {
    loading.value = false
  }
})
</script>
