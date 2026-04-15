<template>
  <nav class="navbar">
    <div class="container navbar-inner">
      <router-link to="/" class="navbar-brand">i<span>K</span>F</router-link>

      <div class="navbar-nav">
        <router-link to="/" :class="{ active: $route.path === '/' }">首页</router-link>
        <router-link to="/products" :class="{ active: $route.path.startsWith('/products') }">全部产品</router-link>
      </div>

      <div class="navbar-nav" style="flex:1">
        <el-input
          v-model="keyword"
          placeholder="搜索耳机..."
          style="max-width:280px"
          size="default"
          @keyup.enter="search"
          clearable
        >
          <template #suffix>
            <el-icon style="cursor:pointer" @click="search"><Search /></el-icon>
          </template>
        </el-input>
      </div>

      <div class="navbar-actions">
        <!-- Cart -->
        <router-link to="/cart" class="cart-btn">
          <el-icon size="20"><ShoppingCart /></el-icon>
          <span>购物车</span>
          <span v-if="cartStore.count" class="cart-badge">{{ cartStore.count }}</span>
        </router-link>

        <!-- User dropdown -->
        <template v-if="userStore.isLoggedIn">
          <el-dropdown @command="handleCommand">
            <span style="color:white;cursor:pointer;display:flex;align-items:center;gap:6px;font-size:14px">
              <el-avatar :size="28" :src="userStore.user?.avatar" style="background:var(--accent)">
                {{ userStore.user?.username?.[0]?.toUpperCase() }}
              </el-avatar>
              {{ userStore.user?.username }}
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">个人中心</el-dropdown-item>
                <el-dropdown-item command="orders">我的订单</el-dropdown-item>
                <el-dropdown-item v-if="userStore.isAdmin" command="admin" divided>后台管理</el-dropdown-item>
                <el-dropdown-item command="logout" divided>退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </template>
        <template v-else>
          <router-link to="/login">
            <el-button type="primary" size="small" round>登录</el-button>
          </router-link>
          <router-link to="/register">
            <el-button size="small" round style="background:transparent;color:white;border-color:rgba(255,255,255,0.4)">注册</el-button>
          </router-link>
        </template>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'
import { useCartStore } from '@/store/cart'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()
const cartStore = useCartStore()
const keyword = ref('')

function search() {
  router.push({ path: '/products', query: { keyword: keyword.value } })
}

function handleCommand(cmd) {
  if (cmd === 'logout') {
    userStore.logout()
    cartStore.items = []
    ElMessage.success('已退出登录')
    router.push('/')
  } else if (cmd === 'profile') {
    router.push('/user/profile')
  } else if (cmd === 'orders') {
    router.push('/user/orders')
  } else if (cmd === 'admin') {
    window.open('/admin/', '_blank')
  }
}
</script>
