<template>
  <div class="admin-layout">
    <!-- Sidebar -->
    <aside class="admin-sidebar">
      <div class="sidebar-logo">
        i<span>K</span>F
        <small>管理后台</small>
      </div>
      <nav class="sidebar-menu">
        <div class="menu-section">概览</div>
        <router-link to="/admin/dashboard" :class="['menu-item', { active: $route.path === '/admin/dashboard' }]">
          <el-icon><DataLine /></el-icon> 数据概览
        </router-link>

        <div class="menu-section">商品</div>
        <router-link to="/admin/products" :class="['menu-item', { active: $route.path === '/admin/products' }]">
          <el-icon><Box /></el-icon> 商品管理
        </router-link>
        <router-link to="/admin/categories" :class="['menu-item', { active: $route.path === '/admin/categories' }]">
          <el-icon><Menu /></el-icon> 分类管理
        </router-link>

        <div class="menu-section">运营</div>
        <router-link to="/admin/orders" :class="['menu-item', { active: $route.path === '/admin/orders' }]">
          <el-icon><List /></el-icon> 订单管理
        </router-link>
        <router-link to="/admin/users" :class="['menu-item', { active: $route.path === '/admin/users' }]">
          <el-icon><User /></el-icon> 用户管理
        </router-link>
        <router-link to="/admin/banners" :class="['menu-item', { active: $route.path === '/admin/banners' }]">
          <el-icon><Picture /></el-icon> 轮播图管理
        </router-link>
      </nav>
    </aside>

    <!-- Main -->
    <div class="admin-main">
      <header class="admin-header">
        <span class="header-title">{{ routeTitle }}</span>
        <div class="header-actions">
          <el-button link @click="() => window.open('/', '_blank')">
            <el-icon><Monitor /></el-icon> 前台预览
          </el-button>
          <el-dropdown @command="handleCmd">
            <span style="cursor:pointer;display:flex;align-items:center;gap:6px;font-size:14px">
              <el-avatar :size="28" style="background:var(--accent)">
                {{ adminStore.user?.username?.[0]?.toUpperCase() }}
              </el-avatar>
              {{ adminStore.user?.username }}
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </header>

      <main class="admin-content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAdminStore } from '@/store/admin'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const adminStore = useAdminStore()

const titleMap = {
  '/admin/dashboard': '数据概览',
  '/admin/products': '商品管理',
  '/admin/categories': '分类管理',
  '/admin/orders': '订单管理',
  '/admin/users': '用户管理',
  '/admin/banners': '轮播图管理',
}

const routeTitle = computed(() => titleMap[route.path] || '管理后台')

function handleCmd(cmd) {
  if (cmd === 'logout') {
    adminStore.logout()
    ElMessage.success('已退出登录')
    router.push('/admin/login')
  }
}

const window = globalThis
</script>
