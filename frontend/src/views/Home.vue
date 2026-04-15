<template>
  <div>
    <!-- Banner -->
    <div class="banner-section" v-if="banners.length">
      <div class="banner-swiper">
        <div class="banner-slide" :style="{ display: currentBanner === i ? 'block' : 'none' }"
          v-for="(b, i) in banners" :key="b.id">
          <img :src="b.image" :alt="b.title" />
          <div class="banner-overlay">
            <div class="banner-text">
              <h2>{{ b.title }}</h2>
              <p>探索 iKF 年度最佳音频产品</p>
              <el-button type="primary" size="large" round @click="$router.push('/products')">
                立即选购
              </el-button>
            </div>
          </div>
        </div>
      </div>
      <!-- dots -->
      <div class="banner-dots">
        <span v-for="(b, i) in banners" :key="i"
          :class="['dot', { active: currentBanner === i }]"
          @click="currentBanner = i" />
      </div>
    </div>
    <div v-else class="default-banner">
      <div class="container">
        <div class="banner-text" style="max-width:600px;padding:80px 0">
          <h2>只做有趣的音乐产品</h2>
          <p>用先锋设计与前沿科技，点燃对音乐的热爱</p>
          <el-button type="primary" size="large" round @click="$router.push('/products')">探索产品</el-button>
        </div>
      </div>
    </div>

    <!-- Categories -->
    <div class="container" style="margin-top:48px">
      <h2 class="section-title">产品系列</h2>
      <div class="category-tabs">
        <div
          v-for="cat in categories" :key="cat.id"
          class="category-tab"
          @click="$router.push(`/products?category_id=${cat.id}`)"
        >
          <div class="cat-icon">{{ cat.icon || '🎧' }}</div>
          <span>{{ cat.name }}</span>
        </div>
      </div>
    </div>

    <!-- Featured Products -->
    <div class="container" style="margin-top:48px">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:24px">
        <h2 class="section-title" style="margin-bottom:0">精选推荐</h2>
        <router-link to="/products" style="color:var(--accent);font-size:14px">查看全部 →</router-link>
      </div>
      <div v-if="loading" class="products-grid">
        <el-skeleton v-for="i in 4" :key="i" style="border-radius:12px" animated>
          <template #template>
            <el-skeleton-item variant="image" style="height:220px" />
            <div style="padding:14px">
              <el-skeleton-item variant="p" style="width:100%" />
              <el-skeleton-item variant="p" style="width:60%;margin-top:8px" />
            </div>
          </template>
        </el-skeleton>
      </div>
      <div v-else class="products-grid">
        <ProductCard v-for="p in featuredProducts" :key="p.id" :product="p" />
      </div>
    </div>

    <!-- All New Products -->
    <div class="container" style="margin-top:48px;margin-bottom:60px">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:24px">
        <h2 class="section-title" style="margin-bottom:0">最新上架</h2>
        <router-link to="/products" style="color:var(--accent);font-size:14px">查看全部 →</router-link>
      </div>
      <div class="products-grid">
        <ProductCard v-for="p in newProducts" :key="p.id" :product="p" />
      </div>
    </div>

    <!-- Brand Values -->
    <div style="background:var(--primary);color:white;padding:60px 0">
      <div class="container">
        <h2 style="text-align:center;margin-bottom:40px;font-size:24px">为什么选择 iKF</h2>
        <div class="values-grid">
          <div class="value-item" v-for="v in values" :key="v.title">
            <div class="value-icon">{{ v.icon }}</div>
            <h3>{{ v.title }}</h3>
            <p>{{ v.desc }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { productApi } from '@/api'
import ProductCard from '@/components/ProductCard.vue'

const banners = ref([])
const categories = ref([])
const featuredProducts = ref([])
const newProducts = ref([])
const loading = ref(true)
const currentBanner = ref(0)

let bannerTimer = null

const values = [
  { icon: '🎵', title: '专业音质', desc: '每款产品均经过专业调音师精心调校，还原最真实的音乐' },
  { icon: '🔋', title: '超长续航', desc: '先进电池技术，单次充电享受全天候音乐体验' },
  { icon: '🛡️', title: '品质保障', desc: '严格质量管控，每款产品出厂前经过100+项测试' },
  { icon: '🚀', title: '极速发货', desc: '下单后24小时内发货，支持顺丰闪送' },
]

onMounted(async () => {
  const [bannersRes, catsRes] = await Promise.all([
    productApi.banners(),
    productApi.categories(),
  ])
  banners.value = bannersRes
  categories.value = catsRes

  if (banners.value.length > 1) {
    bannerTimer = setInterval(() => {
      currentBanner.value = (currentBanner.value + 1) % banners.value.length
    }, 4000)
  }

  const [featuredRes, newRes] = await Promise.all([
    productApi.list({ featured: true, page_size: 4 }),
    productApi.list({ page_size: 8 }),
  ])
  featuredProducts.value = featuredRes.items
  newProducts.value = newRes.items
  loading.value = false
})

onUnmounted(() => {
  if (bannerTimer) clearInterval(bannerTimer)
})
</script>

<style scoped>
.default-banner {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  color: white;
}

.banner-section { position: relative; }

.banner-dots {
  position: absolute;
  bottom: 16px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 8px;
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: rgba(255,255,255,0.5);
  cursor: pointer;
  transition: background 0.2s;
}

.dot.active { background: white; width: 24px; border-radius: 4px; }

.category-tabs {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 16px;
}

.category-tab {
  background: white;
  border-radius: 12px;
  padding: 24px 16px;
  text-align: center;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  transition: all 0.2s;
}

.category-tab:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.1);
  color: var(--accent);
}

.cat-icon {
  font-size: 36px;
  margin-bottom: 10px;
}

.category-tab span {
  font-size: 14px;
  font-weight: 500;
}

.values-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 32px;
  text-align: center;
}

.value-icon { font-size: 40px; margin-bottom: 16px; }

.value-item h3 { font-size: 16px; margin-bottom: 8px; }

.value-item p {
  font-size: 13px;
  color: rgba(255,255,255,0.7);
  line-height: 1.6;
}

@media (max-width: 768px) {
  .category-tabs { grid-template-columns: repeat(3, 1fr); }
  .values-grid { grid-template-columns: repeat(2, 1fr); gap: 20px; }
}
</style>
