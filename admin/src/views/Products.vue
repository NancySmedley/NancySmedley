<template>
  <div class="page-card">
    <div class="page-card-header">
      <span class="page-card-title">商品管理</span>
      <el-button type="primary" @click="openDialog()">+ 添加商品</el-button>
    </div>

    <!-- Filters -->
    <div style="display:flex;gap:12px;margin-bottom:16px">
      <el-input v-model="filters.keyword" placeholder="搜索商品名称" style="width:220px" clearable @change="fetchProducts" />
      <el-select v-model="filters.category_id" placeholder="分类筛选" clearable style="width:160px" @change="fetchProducts">
        <el-option v-for="c in categories" :key="c.id" :label="c.name" :value="c.id" />
      </el-select>
      <el-button @click="fetchProducts">搜索</el-button>
    </div>

    <el-table :data="products" v-loading="loading" stripe>
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column label="封面" width="70">
        <template #default="{ row }">
          <el-image :src="row.cover_image" style="width:50px;height:50px;border-radius:6px;object-fit:cover" />
        </template>
      </el-table-column>
      <el-table-column prop="name" label="商品名称" min-width="180" show-overflow-tooltip />
      <el-table-column label="价格" width="100">
        <template #default="{ row }">
          <span style="color:var(--accent);font-weight:600">¥{{ row.price }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="stock" label="库存" width="80" />
      <el-table-column prop="sales" label="销量" width="80" />
      <el-table-column label="状态" width="80">
        <template #default="{ row }">
          <el-tag :type="row.is_active ? 'success' : 'info'" size="small">{{ row.is_active ? '上架' : '下架' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="精选" width="80">
        <template #default="{ row }">
          <el-tag :type="row.is_featured ? 'warning' : 'info'" size="small">{{ row.is_featured ? '是' : '否' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="140" fixed="right">
        <template #default="{ row }">
          <el-button link type="primary" @click="openDialog(row)">编辑</el-button>
          <el-button link type="danger" @click="deleteProduct(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <div style="margin-top:16px;text-align:right">
      <el-pagination background layout="total, prev, pager, next"
        :total="total" :page-size="pageSize"
        v-model:current-page="page" @current-change="fetchProducts"
      />
    </div>

    <!-- Dialog -->
    <el-dialog v-model="showDialog" :title="editId ? '编辑商品' : '添加商品'" width="680px" top="5vh">
      <el-form :model="form" label-width="90px">
        <el-row :gutter="16">
          <el-col :span="16">
            <el-form-item label="商品名称"><el-input v-model="form.name" /></el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="分类">
              <el-select v-model="form.category_id" placeholder="选择分类" style="width:100%">
                <el-option v-for="c in categories" :key="c.id" :label="c.name" :value="c.id" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="商品描述">
          <el-input v-model="form.description" type="textarea" :rows="3" />
        </el-form-item>
        <el-row :gutter="16">
          <el-col :span="8">
            <el-form-item label="售价（¥）"><el-input-number v-model="form.price" :min="0" :precision="2" style="width:100%" /></el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="原价（¥）"><el-input-number v-model="form.original_price" :min="0" :precision="2" style="width:100%" /></el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="库存"><el-input-number v-model="form.stock" :min="0" style="width:100%" /></el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="封面图片">
          <div style="display:flex;gap:12px;align-items:center">
            <el-input v-model="form.cover_image" placeholder="图片URL 或上传" style="flex:1" />
            <el-upload :show-file-list="false" :before-upload="f => uploadImg(f, 'cover_image')">
              <el-button>上传</el-button>
            </el-upload>
          </div>
          <el-image v-if="form.cover_image" :src="form.cover_image" style="width:80px;height:80px;border-radius:6px;margin-top:8px;object-fit:cover" />
        </el-form-item>
        <el-form-item label="规格参数">
          <el-input v-model="form.specs" type="textarea" :rows="3" placeholder='JSON格式，如: {"品牌":"iKF","续航":"8小时"}' />
        </el-form-item>
        <el-row :gutter="16">
          <el-col :span="6">
            <el-form-item label="是否上架"><el-switch v-model="form.is_active" /></el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="精选推荐"><el-switch v-model="form.is_featured" /></el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="排序权重"><el-input-number v-model="form.sort_order" style="width:100%" /></el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <template #footer>
        <el-button @click="showDialog = false">取消</el-button>
        <el-button type="primary" @click="saveProduct" :loading="saving">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { adminApi } from '@/api'
import { ElMessage, ElMessageBox } from 'element-plus'

const products = ref([])
const categories = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = 20
const loading = ref(false)
const showDialog = ref(false)
const saving = ref(false)
const editId = ref(null)

const filters = reactive({ keyword: '', category_id: null })
const form = ref(defaultForm())

function defaultForm() {
  return {
    name: '', description: '', price: 0, original_price: null, stock: 0,
    cover_image: '', images: '', specs: '', category_id: null,
    is_active: true, is_featured: false, sort_order: 0
  }
}

async function fetchProducts() {
  loading.value = true
  try {
    const params = { page: page.value, page_size: pageSize }
    if (filters.keyword) params.keyword = filters.keyword
    if (filters.category_id) params.category_id = filters.category_id
    const res = await adminApi.products(params)
    products.value = res.items
    total.value = res.total
  } finally {
    loading.value = false
  }
}

async function uploadImg(file, field) {
  const res = await adminApi.upload(file)
  form.value[field] = res.url
  return false
}

function openDialog(row = null) {
  editId.value = row?.id || null
  form.value = row ? { ...defaultForm(), ...row } : defaultForm()
  showDialog.value = true
}

async function saveProduct() {
  if (!form.value.name || form.value.price == null) return ElMessage.warning('请填写商品名称和价格')
  saving.value = true
  try {
    if (editId.value) {
      await adminApi.updateProduct(editId.value, form.value)
    } else {
      await adminApi.createProduct(form.value)
    }
    ElMessage.success('保存成功')
    showDialog.value = false
    await fetchProducts()
  } finally {
    saving.value = false
  }
}

async function deleteProduct(id) {
  await ElMessageBox.confirm('确定删除此商品？删除后不可恢复', '警告', { type: 'warning' })
  await adminApi.deleteProduct(id)
  ElMessage.success('删除成功')
  await fetchProducts()
}

onMounted(async () => {
  categories.value = await adminApi.categories()
  await fetchProducts()
})
</script>
