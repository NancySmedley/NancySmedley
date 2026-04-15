<template>
  <div style="background:white;border-radius:12px;padding:28px;box-shadow:var(--shadow)">
    <h3 style="font-size:18px;font-weight:600;margin-bottom:20px">我的订单</h3>

    <el-tabs v-model="activeStatus" @tab-change="fetchOrders">
      <el-tab-pane label="全部" name="" />
      <el-tab-pane label="待支付" name="pending" />
      <el-tab-pane label="已支付" name="paid" />
      <el-tab-pane label="已发货" name="shipped" />
      <el-tab-pane label="已完成" name="delivered" />
      <el-tab-pane label="已取消" name="cancelled" />
    </el-tabs>

    <div v-if="loading">
      <el-skeleton v-for="i in 3" :key="i" animated style="margin-bottom:16px">
        <template #template>
          <el-skeleton-item variant="rect" style="height:100px;border-radius:8px" />
        </template>
      </el-skeleton>
    </div>

    <div v-else-if="orders.length === 0" class="empty-state">
      <el-icon><List /></el-icon>
      <p>暂无订单</p>
      <el-button type="primary" round @click="$router.push('/products')">去购物</el-button>
    </div>

    <div v-else>
      <div v-for="order in orders" :key="order.id" class="order-card">
        <div class="order-header">
          <span style="font-size:13px;color:#666">订单号：{{ order.order_no }}</span>
          <span :class="['order-status', order.status]">{{ statusMap[order.status] }}</span>
        </div>
        <div class="order-items">
          <div v-for="item in order.items" :key="item.id" class="order-item">
            <img :src="item.product_image || 'https://picsum.photos/60/60'" class="order-img" />
            <div style="flex:1">
              <div style="font-size:14px">{{ item.product_name }}</div>
              <div style="font-size:12px;color:#999">x{{ item.quantity }}</div>
            </div>
            <span style="color:var(--accent);font-weight:600">¥{{ (item.price * item.quantity).toFixed(2) }}</span>
          </div>
        </div>
        <div class="order-footer">
          <span style="font-size:13px;color:#666">{{ formatDate(order.created_at) }}</span>
          <div style="display:flex;align-items:center;gap:12px">
            <span>合计：<strong style="color:var(--accent);font-size:16px">¥{{ order.total_amount.toFixed(2) }}</strong></span>
            <el-button
              v-if="order.status === 'pending'"
              size="small" type="danger" plain
              @click="cancelOrder(order.id)"
            >取消订单</el-button>
          </div>
        </div>
      </div>

      <div style="margin-top:20px;text-align:center" v-if="total > pageSize">
        <el-pagination
          background layout="prev, pager, next"
          :total="total" :page-size="pageSize"
          v-model:current-page="page"
          @current-change="fetchOrders"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { orderApi } from '@/api'
import { ElMessage, ElMessageBox } from 'element-plus'

const orders = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = 10
const loading = ref(false)
const activeStatus = ref('')

const statusMap = {
  pending: '待支付', paid: '已支付', shipped: '已发货',
  delivered: '已完成', cancelled: '已取消'
}

function formatDate(d) {
  return new Date(d).toLocaleString('zh-CN')
}

async function fetchOrders() {
  loading.value = true
  try {
    const res = await orderApi.list({ page: page.value, page_size: pageSize, status: activeStatus.value || undefined })
    orders.value = res.items
    total.value = res.total
  } finally {
    loading.value = false
  }
}

async function cancelOrder(id) {
  await ElMessageBox.confirm('确定要取消这个订单吗？', '提示', { type: 'warning' })
  await orderApi.cancel(id)
  ElMessage.success('订单已取消')
  await fetchOrders()
}

onMounted(fetchOrders)
</script>

<style scoped>
.order-card {
  border: 1px solid #eee;
  border-radius: 10px;
  margin-bottom: 16px;
  overflow: hidden;
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: #f9f9f9;
  border-bottom: 1px solid #eee;
}

.order-status {
  font-size: 13px;
  font-weight: 500;
  padding: 2px 10px;
  border-radius: 4px;
}
.order-status.pending { background: #fff7e6; color: #fa8c16; }
.order-status.paid { background: #e6f4ff; color: #1890ff; }
.order-status.shipped { background: #f0f5ff; color: #2f54eb; }
.order-status.delivered { background: #f6ffed; color: #52c41a; }
.order-status.cancelled { background: #f5f5f5; color: #999; }

.order-items { padding: 12px 16px; }

.order-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 0;
  border-bottom: 1px solid #f5f5f5;
}

.order-img {
  width: 50px;
  height: 50px;
  object-fit: cover;
  border-radius: 6px;
}

.order-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: #fafafa;
  border-top: 1px solid #eee;
}
</style>
