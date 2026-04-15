<template>
  <div class="product-card" @click="$router.push(`/products/${product.id}`)">
    <div style="position:relative">
      <img
        :src="product.cover_image || 'https://picsum.photos/400/400?random=' + product.id"
        :alt="product.name"
        class="product-card-img"
        loading="lazy"
      />
      <span v-if="product.is_featured" class="tag-featured" style="position:absolute;top:10px;left:10px">
        精选
      </span>
      <span v-if="product.original_price && product.original_price > product.price"
        style="position:absolute;top:10px;right:10px;background:var(--accent);color:white;font-size:12px;padding:2px 8px;border-radius:20px">
        省 ¥{{ (product.original_price - product.price).toFixed(0) }}
      </span>
    </div>
    <div class="product-card-body">
      <div class="product-card-name">{{ product.name }}</div>
      <div class="product-card-price">
        <span class="price-now">¥{{ product.price.toFixed(2) }}</span>
        <span v-if="product.original_price" class="price-old">¥{{ product.original_price.toFixed(2) }}</span>
      </div>
      <div class="product-card-bottom">
        <span class="sold-count">已售 {{ product.sales }}</span>
        <el-button
          type="primary" size="small" round
          @click.stop="addToCart"
          :disabled="product.stock === 0"
        >
          {{ product.stock === 0 ? '已售罄' : '加购' }}
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useCartStore } from '@/store/cart'
import { useUserStore } from '@/store/user'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const props = defineProps({ product: Object })
const cartStore = useCartStore()
const userStore = useUserStore()
const router = useRouter()

async function addToCart() {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录')
    router.push('/login')
    return
  }
  await cartStore.addToCart(props.product.id, 1)
}
</script>
