<template>
  <div class="container" style="padding-top:24px;padding-bottom:60px">
    <div style="display:grid;grid-template-columns:220px 1fr;gap:24px">
      <!-- Sidebar -->
      <aside>
        <div style="background:white;border-radius:12px;padding:24px;box-shadow:var(--shadow);text-align:center">
          <el-avatar :size="72" :src="userStore.user?.avatar" style="background:var(--accent);font-size:28px">
            {{ userStore.user?.username?.[0]?.toUpperCase() }}
          </el-avatar>
          <div style="font-weight:600;font-size:16px;margin:12px 0 4px">{{ userStore.user?.username }}</div>
          <div style="font-size:13px;color:#999">{{ userStore.user?.email }}</div>
        </div>
        <div style="background:white;border-radius:12px;margin-top:16px;box-shadow:var(--shadow);overflow:hidden">
          <router-link
            v-for="item in menuItems" :key="item.path"
            :to="item.path"
            :class="['menu-item', { active: $route.path === item.path }]"
          >
            <el-icon><component :is="item.icon" /></el-icon>
            {{ item.label }}
          </router-link>
        </div>
      </aside>

      <!-- Content -->
      <div>
        <router-view />
      </div>
    </div>
  </div>
</template>

<script setup>
import { useUserStore } from '@/store/user'

const userStore = useUserStore()
const menuItems = [
  { path: '/user/profile', label: '个人信息', icon: 'User' },
  { path: '/user/orders', label: '我的订单', icon: 'List' },
  { path: '/user/addresses', label: '收货地址', icon: 'Location' },
]
</script>

<style scoped>
.menu-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 20px;
  font-size: 14px;
  color: #555;
  border-bottom: 1px solid #f5f5f5;
  transition: all 0.2s;
}
.menu-item:hover { color: var(--accent); background: #fff5f5; }
.menu-item.active { color: var(--accent); background: #fff0f0; font-weight: 500; border-left: 3px solid var(--accent); }
</style>
