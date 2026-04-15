<template>
  <div>
    <!-- Stat Cards -->
    <div class="stat-cards" v-loading="loading">
      <div class="stat-card">
        <div class="stat-icon" style="background:#e6f4ff">👥</div>
        <div class="stat-info">
          <div class="value" style="color:#1890ff">{{ stats.total_users }}</div>
          <div class="label">注册用户</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background:#fff7e6">🎧</div>
        <div class="stat-info">
          <div class="value" style="color:#fa8c16">{{ stats.total_products }}</div>
          <div class="label">商品总数</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background:#f6ffed">📦</div>
        <div class="stat-info">
          <div class="value" style="color:#52c41a">{{ stats.total_orders }}</div>
          <div class="label">订单总数</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background:#fff0f0">💰</div>
        <div class="stat-info">
          <div class="value" style="color:#e94560">¥{{ stats.total_revenue?.toFixed(2) }}</div>
          <div class="label">累计收入</div>
        </div>
      </div>
    </div>

    <!-- Recent Orders -->
    <div class="page-card">
      <div class="page-card-header">
        <span class="page-card-title">最近订单</span>
        <router-link to="/admin/orders">
          <el-button link type="primary">查看全部</el-button>
        </router-link>
      </div>
      <el-table :data="stats.recent_orders || []" stripe>
        <el-table-column prop="order_no" label="订单号" width="200" />
        <el-table-column prop="total_amount" label="金额" width="120">
          <template #default="{ row }">
            <span style="color:var(--accent);font-weight:600">¥{{ row.total_amount?.toFixed(2) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="statusType(row.status)" size="small">{{ statusLabel(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="下单时间">
          <template #default="{ row }">{{ new Date(row.created_at).toLocaleString('zh-CN') }}</template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { adminApi } from '@/api'

const stats = ref({ total_users: 0, total_products: 0, total_orders: 0, total_revenue: 0, recent_orders: [] })
const loading = ref(true)

const statusLabel = s => ({ pending: '待支付', paid: '已支付', shipped: '已发货', delivered: '已完成', cancelled: '已取消' }[s] || s)
const statusType = s => ({ pending: 'warning', paid: 'primary', shipped: '', delivered: 'success', cancelled: 'info' }[s] || '')

onMounted(async () => {
  stats.value = await adminApi.stats()
  loading.value = false
})
</script>
