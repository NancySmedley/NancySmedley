<template>
  <div class="static-page">
    <div v-if="loading" style="text-align:center;padding:80px 0;color:#999">加载中...</div>
    <template v-else-if="pageData">
      <div class="static-banner" v-if="bannerImg">
        <img :src="bannerImg" alt="关于我们" />
      </div>
      <div class="container static-content">
        <h1 class="static-title">{{ pageData.title }}</h1>
        <div class="static-body" v-html="pageData.content"></div>
      </div>
    </template>
    <template v-else>
      <img
        src="https://picsum.photos/seed/shinesphere-about/1400/400"
        alt="关于我们"
        class="products-banner"
      />
      <div class="container static-content">
        <h1 class="static-title">关于我们</h1>
        <div class="about-content">
          <div class="about-section">
            <h2>公司简介</h2>
            <p>绚映星球（ShineSphere）成立于2020年，是一家专注于智能音频产品研发、生产与销售的科技公司。公司总部位于中国深圳，拥有完善的研发团队和生产体系。</p>
          </div>
          <div class="about-section">
            <h2>核心优势</h2>
            <ul>
              <li>拥有完整的音频技术自主研发能力，累计获得多项专利</li>
              <li>产品覆盖复古、开放式、蓝牙、睡眠、头戴、游戏电竞等多个系列</li>
              <li>全渠道销售网络，覆盖国内主要电商平台及线下渠道</li>
              <li>严格的品质管控体系，通过多项国内外认证</li>
            </ul>
          </div>
          <div class="about-stats">
            <div class="about-stat-item">
              <div class="about-stat-num">200+</div>
              <div class="about-stat-label">SKU产品</div>
            </div>
            <div class="about-stat-item">
              <div class="about-stat-num">500万+</div>
              <div class="about-stat-label">用户信赖</div>
            </div>
            <div class="about-stat-item">
              <div class="about-stat-num">50+</div>
              <div class="about-stat-label">专利技术</div>
            </div>
            <div class="about-stat-item">
              <div class="about-stat-num">30+</div>
              <div class="about-stat-label">国家和地区</div>
            </div>
          </div>
          <div class="about-section">
            <h2>联系方式</h2>
            <p>服务热线：400-0000-000</p>
            <p>企业邮箱：contact@shinesphere.com</p>
            <p>服务时间：周一至周日 9:00-18:00</p>
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
    pageData.value = await productApi.page('about')
  } catch {
    pageData.value = null
  } finally {
    loading.value = false
  }
})
</script>
