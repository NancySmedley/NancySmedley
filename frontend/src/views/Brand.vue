<template>
  <div class="static-page">
    <div v-if="loading" style="text-align:center;padding:80px 0;color:#999">加载中...</div>
    <template v-else-if="pageData">
      <div class="static-banner" v-if="bannerImg">
        <img :src="bannerImg" alt="品牌文化" />
      </div>
      <div class="container static-content">
        <h1 class="static-title">{{ pageData.title }}</h1>
        <div class="static-body" v-html="pageData.content"></div>
      </div>
    </template>
    <template v-else>
      <!-- Default brand page content -->
      <div class="brand-hero">
        <img src="https://picsum.photos/seed/shinesphere-brand/1400/500" alt="品牌文化" class="products-banner" />
      </div>
      <div class="container static-content">
        <h1 class="static-title">品牌文化</h1>
        <div class="brand-story">
          <div class="brand-section">
            <h2>绚映星球 · ShineSphere</h2>
            <p>绚映星球（ShineSphere）是一家专注于智能音频产品研发与设计的品牌。我们相信，好的声音能让生活更美好，好的设计能让产品与人产生情感连接。</p>
          </div>
          <div class="brand-section">
            <h2>我们的使命</h2>
            <p>为每一位热爱生活、追求品质的用户，提供兼具颜值与性能的智能耳机产品，让科技触手可及，让音乐无处不在。</p>
          </div>
          <div class="brand-section">
            <h2>设计理念</h2>
            <p>ShineSphere的产品设计融合了东方美学与现代科技，每一款产品都经过反复打磨，力求在外观、音质、佩戴舒适度之间找到完美平衡。</p>
          </div>
          <div class="brand-values">
            <div class="brand-value-item">
              <div class="brand-value-icon">✦</div>
              <div class="brand-value-title">品质至上</div>
              <div class="brand-value-desc">严选材料，精工制造，每款产品均经过严格品控</div>
            </div>
            <div class="brand-value-item">
              <div class="brand-value-icon">◎</div>
              <div class="brand-value-title">创新驱动</div>
              <div class="brand-value-desc">持续研发AI降噪、空间音频等前沿音频技术</div>
            </div>
            <div class="brand-value-item">
              <div class="brand-value-icon">◈</div>
              <div class="brand-value-title">用户为本</div>
              <div class="brand-value-desc">深入了解用户需求，为不同场景提供专属解决方案</div>
            </div>
          </div>
        </div>
      </div>
    </template>
    <div class="scroll-top" @click="scrollTop">↑</div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { productApi } from '@/api'

const loading = ref(false)
const pageData = ref(null)

const bannerImg = computed(() => {
  if (!pageData.value?.images) return null
  try {
    const imgs = JSON.parse(pageData.value.images)
    return imgs[0] || null
  } catch { return null }
})

function scrollTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

onMounted(async () => {
  loading.value = true
  try {
    pageData.value = await productApi.page('brand')
  } catch {
    pageData.value = null
  } finally {
    loading.value = false
  }
})
</script>
