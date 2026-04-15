<template>
  <div class="page-card">
    <div class="page-card-header">
      <span class="page-card-title">订单管理</span>
    </div>

    <div style="display:flex;gap:12px;margin-bottom:16px">
      <el-select v-model="filters.status" placeholder="全部状态" clearable style="width:160px" @change="fetchOrders">
        <el-option v-for="(label, val) in statusMap" :key="val" :label="label" :value="val" />
      </el-select>
      <el-button @click="fetchOrders">刷新</el-button>
    </div>

    <el-table :data="orders" v-loading="loading" stripe>
      <el-table-column prop="order_no" label="订单号" width="200" />
      <el-table-column prop="total_amount" label="金额" width="110">
        <template #default="{ row }">
          <span style="color:var(--accent);font-weight:600">¥{{ row.total_amount?.toFixed(2) }}</span>
        </template>
      </el-table-column>
      <el-table-column label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="statusType(row.status)" size="small">{{ statusMap[row.status] }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="商品" width="120">
        <template #default="{ row }">
          <span>{{ row.items?.length || 0 }} 件商品</span>
        </template>
      </el-table-column>
      <el-table-column label="下单时间" width="170">
        <template #default="{ row }">{{ new Date(row.created_at).toLocaleString('zh-CN') }}</template>
      </el-table-column>
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-select
            :model-value="row.status"
            size="small"
            style="width:120px"
            @change="(v) => updateStatus(row.id, v)"
          >
            <el-option v-for="(label, val) in statusMap" :key="val" :label="label" :value="val" />
          </el-select>
        </template>
      </el-table-column>
    </el-table>

    <div style="margin-top:16px;text-align:right">
      <el-pagination background layout="total, prev, pager, next"
        :total="total" :page-size="pageSize"
        v-model:current-page="page" @current-change="fetchOrders"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { adminApi } from '@/api'
import { ElMessage } from 'element-plus'

const orders = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = 20
const loading = ref(false)
const filters = reactive({ status: '' })

const statusMap = { pending: '待支付', paid: '已支付', shipped: '已发货', delivered: '已完成', cancelled: '已取消' }
const statusType = s => ({ pending: 'warning', paid: 'primary', shipped: '', delivered: 'success', cancelled: 'info' }[s] || '')

async function fetchOrders() {
  loading.value = true
  try {
    const params = { page: page.value, page_size: pageSize }
    if (filters.status) params.status = filters.status
    const res = await adminApi.orders(params)
    orders.value = res.items
    total.value = res.total
  } finally {
    loading.value = false
  }
}

async function updateStatus(id, status) {
  await adminApi.updateOrderStatus(id, { status })
  ElMessage.success('状态更新成功')
  await fetchOrders()
}

onMounted(fetchOrders)
</script>
