<template>
  <div class="container" style="padding-top:24px;padding-bottom:60px">
    <h2 class="section-title">确认订单</h2>

    <div style="display:grid;grid-template-columns:1fr 340px;gap:24px">
      <div>
        <!-- Address -->
        <div class="card">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px">
            <h3 style="font-size:16px;font-weight:600">收货地址</h3>
            <el-button link type="primary" size="small" @click="showAddressDialog = true">
              + 添加地址
            </el-button>
          </div>
          <div v-if="addresses.length === 0" style="color:#999;font-size:14px">暂无收货地址，请添加</div>
          <div
            v-for="addr in addresses" :key="addr.id"
            :class="['address-item', { selected: selectedAddress === addr.id }]"
            @click="selectedAddress = addr.id"
          >
            <div style="display:flex;align-items:center;gap:12px">
              <el-radio :model-value="selectedAddress" :label="addr.id" @change="selectedAddress = addr.id" />
              <div>
                <div style="font-weight:500">{{ addr.name }} {{ addr.phone }}</div>
                <div style="font-size:13px;color:#666;margin-top:2px">
                  {{ addr.province }}{{ addr.city }}{{ addr.district }}{{ addr.detail }}
                </div>
              </div>
              <span v-if="addr.is_default" style="margin-left:auto;background:#e6f4ff;color:#1890ff;font-size:12px;padding:2px 8px;border-radius:4px">默认</span>
            </div>
          </div>
        </div>

        <!-- Items -->
        <div class="card" style="margin-top:16px">
          <h3 style="font-size:16px;font-weight:600;margin-bottom:16px">商品清单</h3>
          <div v-for="item in checkoutItems" :key="item.id" class="checkout-item">
            <img :src="item.product.cover_image" class="item-img" />
            <div style="flex:1">
              <div style="font-size:14px;font-weight:500">{{ item.product.name }}</div>
              <div style="font-size:13px;color:#999;margin-top:4px">x{{ item.quantity }}</div>
            </div>
            <span style="font-weight:600;color:var(--accent)">¥{{ (item.product.price * item.quantity).toFixed(2) }}</span>
          </div>
        </div>

        <!-- Remark -->
        <div class="card" style="margin-top:16px">
          <h3 style="font-size:16px;font-weight:600;margin-bottom:12px">订单备注</h3>
          <el-input v-model="remark" type="textarea" :rows="2" placeholder="选填：如有特殊要求请备注" />
        </div>
      </div>

      <!-- Summary -->
      <div>
        <div class="card" style="position:sticky;top:80px">
          <h3 style="font-size:16px;font-weight:600;margin-bottom:20px">订单金额</h3>
          <div v-for="item in checkoutItems" :key="item.id" style="display:flex;justify-content:space-between;font-size:13px;margin-bottom:8px;color:#666">
            <span>{{ item.product.name.substring(0, 16) }}... x{{ item.quantity }}</span>
            <span>¥{{ (item.product.price * item.quantity).toFixed(2) }}</span>
          </div>
          <el-divider />
          <div style="display:flex;justify-content:space-between;font-size:14px;margin-bottom:8px">
            <span>运费</span>
            <span style="color:#52c41a">免运费</span>
          </div>
          <div style="display:flex;justify-content:space-between;font-size:20px;font-weight:700;margin:16px 0">
            <span>合计</span>
            <span style="color:var(--accent)">¥{{ totalAmount.toFixed(2) }}</span>
          </div>
          <el-button
            type="primary" size="large" style="width:100%"
            :loading="submitting"
            @click="submitOrder"
          >提交订单</el-button>
        </div>
      </div>
    </div>

    <!-- Address Dialog -->
    <el-dialog v-model="showAddressDialog" title="添加收货地址" width="500px">
      <el-form :model="addressForm" label-width="80px">
        <el-form-item label="收货人"><el-input v-model="addressForm.name" /></el-form-item>
        <el-form-item label="手机号"><el-input v-model="addressForm.phone" /></el-form-item>
        <el-form-item label="省份"><el-input v-model="addressForm.province" /></el-form-item>
        <el-form-item label="城市"><el-input v-model="addressForm.city" /></el-form-item>
        <el-form-item label="区县"><el-input v-model="addressForm.district" /></el-form-item>
        <el-form-item label="详细地址"><el-input v-model="addressForm.detail" type="textarea" /></el-form-item>
        <el-form-item><el-checkbox v-model="addressForm.is_default">设为默认地址</el-checkbox></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddressDialog = false">取消</el-button>
        <el-button type="primary" @click="saveAddress">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCartStore } from '@/store/cart'
import { orderApi, addressApi } from '@/api'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const cartStore = useCartStore()

const addresses = ref([])
const selectedAddress = ref(null)
const remark = ref('')
const submitting = ref(false)
const showAddressDialog = ref(false)
const addressForm = ref({ name: '', phone: '', province: '', city: '', district: '', detail: '', is_default: false })

const itemIds = route.query.items?.split(',').map(Number) || []
const checkoutItems = computed(() => cartStore.items.filter(i => itemIds.includes(i.id)))
const totalAmount = computed(() => checkoutItems.value.reduce((s, i) => s + i.product.price * i.quantity, 0))

async function fetchAddresses() {
  addresses.value = await addressApi.list()
  const def = addresses.value.find(a => a.is_default)
  if (def) selectedAddress.value = def.id
  else if (addresses.value.length) selectedAddress.value = addresses.value[0].id
}

async function saveAddress() {
  await addressApi.create(addressForm.value)
  ElMessage.success('地址添加成功')
  showAddressDialog.value = false
  await fetchAddresses()
}

async function submitOrder() {
  if (!selectedAddress.value) return ElMessage.warning('请选择收货地址')
  if (!checkoutItems.value.length) return ElMessage.warning('请选择商品')

  submitting.value = true
  try {
    const order = await orderApi.create({
      address_id: selectedAddress.value,
      remark: remark.value,
      items: checkoutItems.value.map(i => ({ product_id: i.product_id, quantity: i.quantity }))
    })
    ElMessage.success('订单提交成功！')
    await cartStore.fetchCart()
    router.push(`/user/orders`)
  } finally {
    submitting.value = false
  }
}

onMounted(async () => {
  await cartStore.fetchCart()
  await fetchAddresses()
})
</script>

<style scoped>
.card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: var(--shadow);
}

.address-item {
  border: 2px solid #eee;
  border-radius: 8px;
  padding: 12px 16px;
  margin-bottom: 10px;
  cursor: pointer;
  transition: border-color 0.2s;
}
.address-item.selected { border-color: var(--accent); }

.checkout-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 0;
  border-bottom: 1px solid #f5f5f5;
}

.item-img {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 6px;
}
</style>
