<template>
  <div class="static-page">
    <div v-if="loading" style="text-align:center;padding:80px 0;color:#999">加载中...</div>
    <template v-else-if="pageData">
      <div class="static-banner" v-if="bannerImg">
        <img :src="bannerImg" alt="品牌合作" />
      </div>
      <div class="container static-content">
        <h1 class="static-title">{{ pageData.title }}</h1>
        <div class="static-body" v-html="pageData.content"></div>
      </div>
    </template>
    <template v-else>
      <img
        src="https://picsum.photos/seed/shinesphere-coop/1400/400"
        alt="品牌合作"
        class="products-banner"
      />
      <div class="container static-content">
        <h1 class="static-title">品牌合作</h1>
        <div class="coop-intro">
          <p>绚映星球（ShineSphere）欢迎与各类品牌、渠道商、媒体展开多元化合作，共同开拓智能音频市场。</p>
        </div>
        <div class="coop-types">
          <div class="coop-type-item">
            <div class="coop-type-icon">🤝</div>
            <div class="coop-type-title">渠道经销</div>
            <div class="coop-type-desc">欢迎全国各地经销商、代理商加入ShineSphere销售网络，共享品牌红利</div>
          </div>
          <div class="coop-type-item">
            <div class="coop-type-icon">🎙️</div>
            <div class="coop-type-title">KOL/KOC合作</div>
            <div class="coop-type-desc">与达人、博主合作推广，欢迎各平台创作者与我们联系</div>
          </div>
          <div class="coop-type-item">
            <div class="coop-type-icon">🏢</div>
            <div class="coop-type-title">企业定制</div>
            <div class="coop-type-desc">为企业客户提供产品定制、品牌联名、大宗采购等服务</div>
          </div>
          <div class="coop-type-item">
            <div class="coop-type-icon">📺</div>
            <div class="coop-type-title">媒体合作</div>
            <div class="coop-type-desc">欢迎各类媒体平台与我们开展内容合作、品牌宣传</div>
          </div>
        </div>
        <div class="coop-contact">
          <h2>联系我们</h2>
          <p>商务合作邮箱：<a href="mailto:contact@shinesphere.com">contact@shinesphere.com</a></p>
          <p>合作热线：400-0000-000（工作日 9:00-18:00）</p>
          <p>微信扫码联系商务专员 →</p>
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
    pageData.value = await productApi.page('cooperation')
  } catch {
    pageData.value = null
  } finally {
    loading.value = false
  }
})
</script>
