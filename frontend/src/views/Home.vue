<template>
  <div>
    <!-- Hero Banner -->
    <div class="hero-banner" v-if="banners.length">
      <div
        v-for="(b, i) in banners" :key="b.id"
        class="hero-slide"
        :class="{ active: current === i, hidden: current !== i }"
        :style="{ background: b.bg_color }"
      >
        <div class="hero-content">
          <div class="hero-tag">{{ b.title }}</div>
          <h1 class="hero-title">{{ b.subtitle }}</h1>
          <div class="hero-features" v-if="parseFeatures(b.features).length">
            <span v-for="f in parseFeatures(b.features)" :key="f">{{ f }}</span>
          </div>
          <div class="hero-btns">
            <button class="btn-new">新品上市</button>
            <button class="btn-buy" @click="openLink(b.link)">{{ b.btn_text || '立即购买' }}</button>
          </div>
        </div>
        <img class="hero-image" :src="b.image" :alt="b.title" />
      </div>

      <div class="hero-dots">
        <div
          v-for="(b, i) in banners" :key="i"
          class="hero-dot" :class="{ active: current === i }"
          @click="current = i"
        />
      </div>
    </div>

    <!-- Hot Sale -->
    <div v-if="featuredProducts.length">
      <div class="section-header">
        <div class="section-en">iKF ACE HOT SALE</div>
        <div class="section-zh">iKF 主销爆款</div>
      </div>
      <div class="hot-sale-list">
        <div
          v-for="(p, i) in featuredProducts" :key="p.id"
          class="hot-item" :class="{ reverse: i % 2 === 1 }"
        >
          <div class="hot-img-wrap">
            <img :src="p.cover_image" :alt="p.name" />
          </div>
          <div class="hot-info">
            <div class="hot-name">
              {{ p.name }}
              <span class="hot-badge" v-if="i === 0">新品</span>
            </div>
            <div class="hot-desc">{{ p.short_desc }}</div>
            <div class="hot-colors" v-if="parseColors(p.colors).length">
              <div
                v-for="c in parseColors(p.colors)" :key="c"
                class="color-dot" :style="{ background: c }"
              />
            </div>
            <a class="link-buy" :href="p.external_link || '#'" target="_blank">立即购买</a>
          </div>
        </div>
      </div>
    </div>

    <!-- Born for Movement -->
    <div v-if="lifestyleProducts.length">
      <div class="section-header">
        <div class="section-en">BORN FOR MOVEMENT</div>
        <div class="section-zh">为运动而生</div>
      </div>
      <div class="lifestyle-section">
        <div v-for="p in lifestyleProducts" :key="p.id" class="lifestyle-item">
          <img :src="p.cover_image" :alt="p.name" />
          <div class="lifestyle-overlay">
            <div class="lifestyle-name">{{ p.name }}</div>
            <div class="lifestyle-desc">{{ p.short_desc }}</div>
            <a class="link-buy" style="color:white" :href="p.external_link || '#'" target="_blank">立即购买</a>
          </div>
        </div>
      </div>
    </div>

    <!-- Fashion -->
    <div v-if="fashionProducts.length" class="container fashion-section">
      <div class="fashion-title">穿搭好物</div>
      <div class="fashion-grid">
        <div
          v-for="p in fashionProducts" :key="p.id"
          class="fashion-card"
          @click="openLink(p.external_link)"
        >
          <img :src="p.cover_image" :alt="p.name" />
          <div class="fashion-card-info">
            <div class="fashion-card-name">{{ p.name }}</div>
            <div class="fashion-card-desc">{{ p.short_desc }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Scroll to top -->
    <div class="scroll-top" @click="scrollTop">↑</div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { productApi } from '@/api'

const banners = ref([])
const featuredProducts = ref([])
const lifestyleProducts = ref([])
const fashionProducts = ref([])
const current = ref(0)
let timer = null

function parseFeatures(str) {
  try { return JSON.parse(str || '[]') } catch { return [] }
}

function parseColors(str) {
  try { return JSON.parse(str || '[]') } catch { return [] }
}

function openLink(url) {
  if (url) window.open(url, '_blank')
}

function scrollTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

onMounted(async () => {
  const [bannersRes, featuredRes, lifestyleRes, fashionRes] = await Promise.all([
    productApi.banners(),
    productApi.list({ featured: true, page_size: 6 }),
    productApi.list({ lifestyle: true, page_size: 4 }),
    productApi.list({ fashion: true, page_size: 3 }),
  ])
  banners.value = bannersRes
  featuredProducts.value = featuredRes.items
  lifestyleProducts.value = lifestyleRes.items
  fashionProducts.value = fashionRes.items

  if (banners.value.length > 1) {
    timer = setInterval(() => {
      current.value = (current.value + 1) % banners.value.length
    }, 5000)
  }
})

onUnmounted(() => { if (timer) clearInterval(timer) })
</script>
