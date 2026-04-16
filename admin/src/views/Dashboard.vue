<template>
  <div>
    <!-- Stat Cards -->
    <div class="stat-cards" v-loading="loading">
      <div class="stat-card">
        <div class="stat-icon" style="background:#e6f4ff">🎧</div>
        <div class="stat-info">
          <div class="value" style="color:#1890ff">{{ stats.total_products }}</div>
          <div class="label">商品总数</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background:#fff7e6">📱</div>
        <div class="stat-info">
          <div class="value" style="color:#fa8c16">{{ stats.total_downloads }}</div>
          <div class="label">软件下载</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background:#f6ffed">📄</div>
        <div class="stat-info">
          <div class="value" style="color:#52c41a">{{ stats.total_manuals }}</div>
          <div class="label">说明书数量</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background:#fff0f0">👥</div>
        <div class="stat-info">
          <div class="value" style="color:#e94560">{{ stats.total_users }}</div>
          <div class="label">注册用户</div>
        </div>
      </div>
    </div>

    <!-- Quick Links -->
    <div class="page-card" style="margin-top:24px">
      <div class="page-card-header">
        <span class="page-card-title">快捷入口</span>
      </div>
      <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:16px;padding:8px 0">
        <router-link to="/admin/products" style="text-decoration:none">
          <div style="padding:20px;background:#f5f5f5;border-radius:8px;text-align:center;cursor:pointer;transition:background .2s">
            <div style="font-size:28px;margin-bottom:8px">🎧</div>
            <div style="font-size:13px;color:#333">商品管理</div>
          </div>
        </router-link>
        <router-link to="/admin/banners" style="text-decoration:none">
          <div style="padding:20px;background:#f5f5f5;border-radius:8px;text-align:center;cursor:pointer">
            <div style="font-size:28px;margin-bottom:8px">🖼️</div>
            <div style="font-size:13px;color:#333">轮播图管理</div>
          </div>
        </router-link>
        <router-link to="/admin/downloads" style="text-decoration:none">
          <div style="padding:20px;background:#f5f5f5;border-radius:8px;text-align:center;cursor:pointer">
            <div style="font-size:28px;margin-bottom:8px">📱</div>
            <div style="font-size:13px;color:#333">软件下载</div>
          </div>
        </router-link>
        <router-link to="/admin/pages" style="text-decoration:none">
          <div style="padding:20px;background:#f5f5f5;border-radius:8px;text-align:center;cursor:pointer">
            <div style="font-size:28px;margin-bottom:8px">📝</div>
            <div style="font-size:13px;color:#333">页面内容</div>
          </div>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { adminApi } from '@/api'

const stats = ref({ total_products: 0, total_downloads: 0, total_manuals: 0, total_users: 0 })
const loading = ref(true)

onMounted(async () => {
  stats.value = await adminApi.stats()
  loading.value = false
})
</script>
