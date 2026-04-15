<template>
  <div class="container" style="padding-top:24px;padding-bottom:60px">
    <h2 class="section-title">购物车</h2>

    <div v-if="cartStore.items.length === 0" class="empty-state">
      <el-icon><ShoppingCart /></el-icon>
      <p>购物车是空的</p>
      <el-button type="primary" round @click="$router.push('/products')">去逛逛</el-button>
    </div>

    <div v-else style="display:grid;grid-template-columns:1fr 320px;gap:24px">
      <!-- Cart Items -->
      <div>
        <div style="background:white;border-radius:12px;padding:20px;box-shadow:var(--shadow)">
          <!-- Select All -->
          <div style="display:flex;align-items:center;padding-bottom:16px;border-bottom:1px solid #eee;margin-bottom:16px">
            <el-checkbox
              :model-value="allSelected"
              @change="cartStore.toggleSelectAll"
            >全选</el-checkbox>
            <el-button
              link type="danger" size="small" style="margin-left:auto"
              @click="removeSelected"
            >删除所选</el-button>
          </div>

          <!-- Items -->
          <div v-for="item in cartStore.items" :key="item.id" class="cart-item">
            <el-checkbox
              :model-value="item.selected"
              @change="cartStore.toggleSelect(item.id)"
            />
            <img
              :src="item.product.cover_image"
              class="item-img"
              @click="$router.push(`/products/${item.product.id}`)"
            />
            <div class="item-info">
              <div class="item-name" @click="$router.push(`/products/${item.product.id}`)">
                {{ item.product.name }}
              </div>
              <div style="color:#999;font-size:12px">库存 {{ item.product.stock }} 件</div>
            </div>
            <div class="item-price">¥{{ item.product.price.toFixed(2) }}</div>
            <el-input-number
              :model-value="item.quantity"
              :min="1"
              :max="item.product.stock"
              size="small"
              @change="(val) => updateQty(item.id, val)"
            />
            <div class="item-subtotal">¥{{ (item.product.price * item.quantity).toFixed(2) }}</div>
            <el-button link type="danger" @click="cartStore.removeItem(item.id)">
              <el-icon><Delete /></el-icon>
            </el-button>
          </div>
        </div>
      </div>

      <!-- Summary -->
      <div>
        <div style="background:white;border-radius:12px;padding:24px;box-shadow:var(--shadow);position:sticky;top:80px">
          <h3 style="margin-bottom:20px;font-size:16px;font-weight:600">订单摘要</h3>
          <div style="display:flex;justify-content:space-between;margin-bottom:12px;font-size:14px">
            <span>已选 {{ selectedCount }} 件</span>
            <span>小计：<strong style="color:var(--accent)">¥{{ cartStore.selectedTotal.toFixed(2) }}</strong></span>
          </div>
          <div style="display:flex;justify-content:space-between;margin-bottom:12px;font-size:14px">
            <span>运费</span>
            <span style="color:#52c41a">免运费</span>
          </div>
          <el-divider />
          <div style="display:flex;justify-content:space-between;font-size:18px;font-weight:700;margin-bottom:20px">
            <span>合计</span>
            <span style="color:var(--accent)">¥{{ cartStore.selectedTotal.toFixed(2) }}</span>
          </div>
          <el-button
            type="primary" size="large" style="width:100%;font-size:16px"
            :disabled="selectedCount === 0"
            @click="checkout"
          >去结算 ({{ selectedCount }})</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore } from '@/store/cart'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const cartStore = useCartStore()

const allSelected = computed(() => cartStore.items.every(i => i.selected))
const selectedCount = computed(() => cartStore.items.filter(i => i.selected).reduce((s, i) => s + i.quantity, 0))

async function updateQty(itemId, qty) {
  await cartStore.updateQuantity(itemId, qty)
}

async function removeSelected() {
  const selected = cartStore.items.filter(i => i.selected)
  if (!selected.length) return ElMessage.warning('请先选择要删除的商品')
  await ElMessageBox.confirm(`确定删除所选 ${selected.length} 件商品？`, '提示', { type: 'warning' })
  for (const item of selected) {
    await cartStore.removeItem(item.id)
  }
}

function checkout() {
  const selected = cartStore.items.filter(i => i.selected)
  if (!selected.length) return ElMessage.warning('请先选择商品')
  const ids = selected.map(i => i.id).join(',')
  router.push({ path: '/checkout', query: { items: ids } })
}
</script>

<style scoped>
.cart-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 0;
  border-bottom: 1px solid #f5f5f5;
}

.item-img {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 8px;
  cursor: pointer;
}

.item-info { flex: 1; }

.item-name {
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  margin-bottom: 4px;
}

.item-name:hover { color: var(--accent); }

.item-price { color: var(--accent); font-weight: 600; width: 80px; text-align: center; }

.item-subtotal { font-weight: 700; width: 80px; text-align: center; color: var(--accent); }
</style>
