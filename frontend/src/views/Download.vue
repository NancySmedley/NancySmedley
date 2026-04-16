<template>
  <div class="static-page">
    <img
      src="https://picsum.photos/seed/shinesphere-download/1400/300"
      alt="软件下载"
      class="products-banner"
    />
    <div class="container static-content">
      <h1 class="static-title">软件下载</h1>
      <div v-if="loading" style="text-align:center;padding:60px 0;color:#999">加载中...</div>
      <div v-else-if="!downloads.length" style="text-align:center;padding:60px 0;color:#999">暂无下载</div>
      <div v-else class="download-list">
        <div v-for="d in downloads" :key="d.id" class="download-card">
          <div class="download-icon">
            <img v-if="d.cover_image" :src="d.cover_image" :alt="d.name" />
            <div v-else class="download-icon-placeholder">📱</div>
          </div>
          <div class="download-info">
            <div class="download-name">{{ d.name }}</div>
            <div class="download-desc" v-if="d.description">{{ d.description }}</div>
            <div class="download-version" v-if="d.version">版本：{{ d.version }}</div>
          </div>
          <div class="download-btns">
            <a v-if="d.ios_url" :href="d.ios_url" target="_blank" class="dl-btn dl-ios">
              <span>iOS 下载</span>
            </a>
            <a v-if="d.android_url" :href="d.android_url" target="_blank" class="dl-btn dl-android">
              <span>Android 下载</span>
            </a>
            <a v-if="d.windows_url" :href="d.windows_url" target="_blank" class="dl-btn dl-win">
              <span>Windows 下载</span>
            </a>
            <a v-if="d.mac_url" :href="d.mac_url" target="_blank" class="dl-btn dl-mac">
              <span>macOS 下载</span>
            </a>
          </div>
        </div>
      </div>
    </div>
    <div class="scroll-top" @click="scrollTop">↑</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { productApi } from '@/api'

const downloads = ref([])
const loading = ref(false)

function scrollTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

onMounted(async () => {
  loading.value = true
  try {
    downloads.value = await productApi.downloads()
  } catch {
    downloads.value = []
  } finally {
    loading.value = false
  }
})
</script>
