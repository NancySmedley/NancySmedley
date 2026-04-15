<template>
  <div class="container" style="padding-top:24px;padding-bottom:60px" v-loading="loading">
    <div class="breadcrumb">
      <router-link to="/">首页</router-link> /
      <router-link to="/products">产品</router-link> /
      {{ product?.name }}
    </div>

    <div v-if="product" class="detail-wrap">
      <!-- Left: Images -->
      <div class="detail-images">
        <div class="main-img-wrap">
          <img :src="currentImage || product.cover_image" :alt="product.name" class="main-img" />
        </div>
        <div class="thumb-list">
          <div
            v-for="(img, i) in allImages" :key="i"
            :class="['thumb', { active: currentImage === img }]"
            @click="currentImage = img"
          >
            <img :src="img" :alt="'图片' + i" />
          </div>
        </div>
      </div>

      <!-- Right: Info -->
      <div class="detail-info">
        <div style="display:flex;gap:8px;margin-bottom:12px">
          <span v-if="product.is_featured" class="tag-featured">精选</span>
          <span v-if="product.category" style="background:#f0f0f0;color:#666;font-size:12px;padding:2px 10px;border-radius:4px">
            {{ product.category.name }}
          </span>
        </div>

        <h1 class="product-title">{{ product.name }}</h1>
        <p class="product-desc">{{ product.description }}</p>

        <div class="price-block">
          <span class="price-big">¥{{ product.price.toFixed(2) }}</span>
          <span v-if="product.original_price" class="price-origin">¥{{ product.original_price.toFixed(2) }}</span>
          <span v-if="product.original_price" class="price-save">
            节省 ¥{{ (product.original_price - product.price).toFixed(2) }}
          </span>
        </div>

        <div class="info-row">
          <span class="info-label">库存</span>
          <span :style="{ color: product.stock > 0 ? '#52c41a' : '#ff4d4f' }">
            {{ product.stock > 0 ? `${product.stock} 件` : '暂时缺货' }}
          </span>
        </div>
        <div class="info-row">
          <span class="info-label">已售</span>
          <span>{{ product.sales }} 件</span>
        </div>

        <div class="quantity-row">
          <span class="info-label">数量</span>
          <el-input-number
            v-model="quantity"
            :min="1"
            :max="product.stock"
            :disabled="product.stock === 0"
          />
        </div>

        <div class="action-row">
          <el-button
            type="primary" size="large" style="flex:1"
            :disabled="product.stock === 0"
            @click="addToCart"
          >
            <el-icon><ShoppingCart /></el-icon>
            加入购物车
          </el-button>
          <el-button
            size="large" style="flex:1;background:var(--accent);color:white;border-color:var(--accent)"
            :disabled="product.stock === 0"
            @click="buyNow"
          >
            立即购买
          </el-button>
        </div>

        <!-- Specs -->
        <div v-if="specs && Object.keys(specs).length" class="specs-block">
          <h3 style="font-size:15px;font-weight:600;margin-bottom:14px">产品规格</h3>
          <table class="specs-table">
            <tr v-for="(val, key) in specs" :key="key">
              <td class="spec-key">{{ key }}</td>
              <td>{{ val }}</td>
            </tr>
          </table>
        </div>
      </div>
    </div>

    <!-- Related Products -->
    <div v-if="related.length" style="margin-top:48px">
      <h2 class="section-title">相关产品</h2>
      <div class="products-grid">
        <ProductCard v-for="p in related" :key="p.id" :product="p" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { productApi, cartApi } from '@/api'
import { useCartStore } from '@/store/cart'
import { useUserStore } from '@/store/user'
import { ElMessage } from 'element-plus'
import ProductCard from '@/components/ProductCard.vue'

const route = useRoute()
const router = useRouter()
const cartStore = useCartStore()
const userStore = useUserStore()

const product = ref(null)
const loading = ref(true)
const currentImage = ref('')
const quantity = ref(1)
const related = ref([])

const allImages = computed(() => {
  const imgs = []
  if (product.value?.cover_image) imgs.push(product.value.cover_image)
  try {
    const extra = JSON.parse(product.value?.images || '[]')
    extra.forEach(img => { if (!imgs.includes(img)) imgs.push(img) })
  } catch {}
  return imgs
})

const specs = computed(() => {
  try { return JSON.parse(product.value?.specs || '{}') } catch { return {} }
})

async function addToCart() {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录')
    return router.push('/login')
  }
  await cartStore.addToCart(product.value.id, quantity.value)
}

async function buyNow() {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录')
    return router.push('/login')
  }
  await cartStore.addToCart(product.value.id, quantity.value)
  router.push('/cart')
}

onMounted(async () => {
  const id = route.params.id
  product.value = await productApi.detail(id)
  currentImage.value = product.value.cover_image
  loading.value = false

  if (product.value.category_id) {
    const res = await productApi.list({ category_id: product.value.category_id, page_size: 4 })
    related.value = res.items.filter(p => p.id !== product.value.id).slice(0, 4)
  }
})
</script>

<style scoped>
.detail-wrap {
  display: grid;
  grid-template-columns: 480px 1fr;
  gap: 40px;
  margin-top: 20px;
}

.main-img-wrap {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  aspect-ratio: 1;
  box-shadow: var(--shadow);
}

.main-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.main-img:hover { transform: scale(1.03); }

.thumb-list {
  display: flex;
  gap: 10px;
  margin-top: 12px;
  flex-wrap: wrap;
}

.thumb {
  width: 70px;
  height: 70px;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  border: 2px solid transparent;
  transition: border-color 0.2s;
}

.thumb.active { border-color: var(--accent); }
.thumb img { width: 100%; height: 100%; object-fit: cover; }

.product-title {
  font-size: 24px;
  font-weight: 700;
  line-height: 1.4;
  margin-bottom: 12px;
}

.product-desc {
  font-size: 14px;
  color: #666;
  line-height: 1.8;
  margin-bottom: 20px;
}

.price-block {
  display: flex;
  align-items: baseline;
  gap: 12px;
  margin-bottom: 20px;
  padding: 16px;
  background: #fff5f5;
  border-radius: 10px;
}

.price-big { font-size: 32px; font-weight: 700; color: var(--accent); }
.price-origin { font-size: 16px; color: #999; text-decoration: line-through; }
.price-save {
  font-size: 13px;
  background: var(--accent);
  color: white;
  padding: 2px 10px;
  border-radius: 20px;
}

.info-row {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 12px;
  font-size: 14px;
}

.info-label { color: #999; width: 40px; }

.quantity-row {
  display: flex;
  align-items: center;
  gap: 16px;
  margin: 20px 0;
}

.action-row {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
}

.specs-block {
  background: #f9f9f9;
  border-radius: 10px;
  padding: 20px;
}

.specs-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

.specs-table tr { border-bottom: 1px solid #eee; }
.specs-table td { padding: 10px 12px; }
.spec-key { color: #666; width: 120px; }
</style>
