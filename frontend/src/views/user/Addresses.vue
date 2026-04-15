<template>
  <div style="background:white;border-radius:12px;padding:28px;box-shadow:var(--shadow)">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px">
      <h3 style="font-size:18px;font-weight:600">收货地址</h3>
      <el-button type="primary" @click="openDialog()">+ 添加地址</el-button>
    </div>

    <div v-if="!addresses.length" class="empty-state">
      <el-icon><Location /></el-icon>
      <p>还没有收货地址</p>
    </div>

    <div v-else class="address-list">
      <div v-for="addr in addresses" :key="addr.id" class="address-card">
        <div>
          <div style="font-weight:500;margin-bottom:6px">{{ addr.name }} <span style="margin-left:8px;color:#666">{{ addr.phone }}</span></div>
          <div style="font-size:13px;color:#666">{{ addr.province }}{{ addr.city }}{{ addr.district }}{{ addr.detail }}</div>
          <span v-if="addr.is_default" style="margin-top:8px;display:inline-block;background:#e6f4ff;color:#1890ff;font-size:12px;padding:2px 8px;border-radius:4px">默认地址</span>
        </div>
        <div style="display:flex;gap:8px;flex-shrink:0">
          <el-button link @click="openDialog(addr)">编辑</el-button>
          <el-button link type="danger" @click="deleteAddr(addr.id)">删除</el-button>
        </div>
      </div>
    </div>

    <el-dialog v-model="showDialog" :title="editId ? '编辑地址' : '添加地址'" width="500px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="收货人"><el-input v-model="form.name" /></el-form-item>
        <el-form-item label="手机号"><el-input v-model="form.phone" /></el-form-item>
        <el-form-item label="省份"><el-input v-model="form.province" /></el-form-item>
        <el-form-item label="城市"><el-input v-model="form.city" /></el-form-item>
        <el-form-item label="区县"><el-input v-model="form.district" /></el-form-item>
        <el-form-item label="详细地址"><el-input v-model="form.detail" type="textarea" /></el-form-item>
        <el-form-item><el-checkbox v-model="form.is_default">设为默认</el-checkbox></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showDialog = false">取消</el-button>
        <el-button type="primary" @click="save" :loading="saving">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { addressApi } from '@/api'
import { ElMessage, ElMessageBox } from 'element-plus'

const addresses = ref([])
const showDialog = ref(false)
const saving = ref(false)
const editId = ref(null)
const form = ref({ name: '', phone: '', province: '', city: '', district: '', detail: '', is_default: false })

async function fetchAddresses() {
  addresses.value = await addressApi.list()
}

function openDialog(addr = null) {
  editId.value = addr?.id || null
  form.value = addr
    ? { name: addr.name, phone: addr.phone, province: addr.province, city: addr.city, district: addr.district, detail: addr.detail, is_default: addr.is_default }
    : { name: '', phone: '', province: '', city: '', district: '', detail: '', is_default: false }
  showDialog.value = true
}

async function save() {
  saving.value = true
  try {
    if (editId.value) {
      await addressApi.update(editId.value, form.value)
    } else {
      await addressApi.create(form.value)
    }
    ElMessage.success('保存成功')
    showDialog.value = false
    await fetchAddresses()
  } finally {
    saving.value = false
  }
}

async function deleteAddr(id) {
  await ElMessageBox.confirm('确定删除这个地址吗？', '提示', { type: 'warning' })
  await addressApi.remove(id)
  ElMessage.success('删除成功')
  await fetchAddresses()
}

onMounted(fetchAddresses)
</script>

<style scoped>
.address-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border: 1px solid #eee;
  border-radius: 10px;
  margin-bottom: 12px;
}
</style>
