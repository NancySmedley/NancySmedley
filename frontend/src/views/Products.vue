<template>
  <div class="container" style="padding-top:24px;padding-bottom:60px">
    <div class="breadcrumb">首页 / 全部产品</div>

    <div style="display:flex;gap:24px">
      <!-- Sidebar -->
      <aside style="width:200px;flex-shrink:0">
        <div style="background:white;border-radius:12px;padding:20px;box-shadow:var(--shadow)">
          <h3 style="font-size:15px;margin-bottom:16px;font-weight:600">产品分类</h3>
          <div
            :class="['cat-item', { active: !filters.category_id }]"
            @click="setCategory(null)"
          >全部产品</div>
          <div
            v-for="cat in categories" :key="cat.id"
            :class="['cat-item', { active: filters.category_id === cat.id }]"
            @click="setCategory(cat.id)"
          >{{ cat.icon }} {{ cat.name }}</div>
        </div>
      </aside>

      <!-- Main -->
      <div style="flex:1">
        <!-- Toolbar -->
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px">
          <div style="font-size:14px;color:#666">
            共 <strong>{{ total }}</strong> 款产品
          </div>
          <div style="display:flex;gap:12px;align-items:center">
            <el-input
              v-model="filters.keyword"
              placeholder="搜索产品..."
              size="default"
              style="width:200px"
              clearable
              @change="fetchProducts"
            >
              <template #prefix><el-icon><Search /></el-icon></template>
            </el-input>
          </div>
        </div>

        <!-- Grid -->
        <div v-if="loading">
          <div class="products-grid">
            <el-skeleton v-for="i in 8" :key="i" animated>
              <template #template>
                <el-skeleton-item variant="image" style="height:220px;border-radius:12px" />
                <div style="padding:14px 0">
                  <el-skeleton-item variant="p" style="width:100%" />
                  <el-skeleton-item variant="p" style="width:60%;margin-top:8px" />
                </div>
              </template>
            </el-skeleton>
          </div>
        </div>
        <div v-else-if="products.length === 0" class="empty-state">
          <el-icon><Box /></el-icon>
          <p>暂无产品</p>
        </div>
        <div v-else class="products-grid">
          <ProductCard v-for="p in products" :key="p.id" :product="p" />
        </div>

        <!-- Pagination -->
        <div v-if="total > filters.page_size" style="margin-top:32px;text-align:center">
          <el-pagination
            background
            layout="prev, pager, next"
            :total="total"
            :page-size="filters.page_size"
            v-model:current-page="filters.page"
            @current-change="fetchProducts"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { productApi } from '@/api'
import ProductCard from '@/components/ProductCard.vue'

const route = useRoute()
const router = useRouter()

const categories = ref([])
const products = ref([])
const total = ref(0)
const loading = ref(false)

const filters = reactive({
  page: 1,
  page_size: 12,
  category_id: route.query.category_id ? Number(route.query.category_id) : null,
  keyword: route.query.keyword || '',
})

async function fetchProducts() {
  loading.value = true
  try {
    const params = { ...filters }
    if (!params.category_id) delete params.category_id
    if (!params.keyword) delete params.keyword
    const res = await productApi.list(params)
    products.value = res.items
    total.value = res.total
  } finally {
    loading.value = false
  }
}

function setCategory(id) {
  filters.category_id = id
  filters.page = 1
  fetchProducts()
}

watch(() => route.query, (q) => {
  if (q.category_id) filters.category_id = Number(q.category_id)
  if (q.keyword !== undefined) filters.keyword = q.keyword
  fetchProducts()
})

onMounted(async () => {
  categories.value = await productApi.categories()
  await fetchProducts()
})
</script>

<style scoped>
.cat-item {
  padding: 10px 12px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  margin-bottom: 4px;
  transition: all 0.2s;
  color: #555;
}
.cat-item:hover { background: #f5f5f5; color: var(--accent); }
.cat-item.active { background: var(--accent); color: white; font-weight: 500; }
</style>
