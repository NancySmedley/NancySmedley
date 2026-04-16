<template>
  <div class="products-page">
    <!-- 顶部大图 -->
    <img
      src="https://picsum.photos/seed/shinesphere-banner/1400/400"
      alt="ShineSphere 产品系列"
      class="products-banner"
    />

    <div class="container">
      <!-- 系列 Tabs -->
      <div class="series-tabs">
        <div
          class="series-tab"
          :class="{ active: !activeSeries }"
          @click="selectSeries(null)"
        >全部</div>
        <div
          v-for="s in seriesList" :key="s"
          class="series-tab"
          :class="{ active: activeSeries === s }"
          @click="selectSeries(s)"
        >{{ s }}</div>
      </div>

      <!-- 产品网格 -->
      <div v-if="loading" class="product-grid">
        <div v-for="i in 8" :key="i" style="text-align:center">
          <div style="background:#f5f5f5;aspect-ratio:1;border-radius:4px;margin-bottom:12px"></div>
          <div style="height:14px;background:#f0f0f0;border-radius:2px;width:80%;margin:0 auto"></div>
        </div>
      </div>

      <div v-else-if="!products.length" style="text-align:center;padding:80px 0;color:#999">
        暂无产品
      </div>

      <div v-else class="product-grid">
        <div
          v-for="p in products" :key="p.id"
          class="product-card"
          @click="openLink(p.external_link)"
        >
          <div class="product-card-img-wrap">
            <img :src="p.cover_image" :alt="p.name" loading="lazy" />
          </div>
          <div class="product-card-name">{{ p.name }}</div>
        </div>
      </div>

      <!-- 分页 -->
      <div class="pagination" v-if="total > pageSize">
        <button
          class="page-btn"
          :disabled="page === 1"
          @click="changePage(page - 1)"
        >上一页</button>
        <button
          v-for="n in totalPages" :key="n"
          class="page-btn" :class="{ active: page === n }"
          @click="changePage(n)"
        >{{ n }}</button>
        <button
          class="page-btn"
          :disabled="page === totalPages"
          @click="changePage(page + 1)"
        >下一页</button>
      </div>
    </div>

    <div class="scroll-top" @click="scrollTop">↑</div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { productApi } from '@/api'

const route = useRoute()
const products = ref([])
const seriesList = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = 12
const loading = ref(false)
const activeSeries = ref(route.query.series || null)

const totalPages = computed(() => Math.ceil(total.value / pageSize))

function openLink(url) {
  if (url) window.open(url, '_blank')
}

function scrollTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function selectSeries(s) {
  activeSeries.value = s
  page.value = 1
  fetchProducts()
}

function changePage(n) {
  page.value = n
  window.scrollTo({ top: 200, behavior: 'smooth' })
  fetchProducts()
}

async function fetchProducts() {
  loading.value = true
  try {
    const params = { page: page.value, page_size: pageSize }
    if (activeSeries.value) params.series = activeSeries.value
    const res = await productApi.list(params)
    products.value = res.items
    total.value = res.total
  } finally {
    loading.value = false
  }
}

watch(() => route.query.series, (s) => {
  activeSeries.value = s || null
  page.value = 1
  fetchProducts()
})

onMounted(async () => {
  seriesList.value = await productApi.series()
  await fetchProducts()
})
</script>
