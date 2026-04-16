<template>
  <nav class="navbar">
    <div class="container navbar-inner">
      <router-link to="/" class="navbar-logo">
        <div class="logo-circle">✦</div>
        <span>ShineSphere</span>
      </router-link>

      <div class="navbar-nav">
        <router-link to="/" class="nav-link" :class="{ active: $route.path === '/' }">首页</router-link>
        <router-link to="/ai-headphones" class="nav-link" :class="{ active: $route.path === '/ai-headphones' }">Ai耳机</router-link>
        <router-link to="/brand" class="nav-link" :class="{ active: $route.path === '/brand' }">品牌文化</router-link>
        <router-link to="/download" class="nav-link" :class="{ active: $route.path === '/download' }">软件下载</router-link>
        <router-link to="/manual" class="nav-link" :class="{ active: $route.path === '/manual' }">产品说明书</router-link>
        <router-link to="/cooperation" class="nav-link" :class="{ active: $route.path === '/cooperation' }">品牌合作</router-link>
        <router-link to="/about" class="nav-link" :class="{ active: $route.path === '/about' }">关于我们</router-link>
      </div>
    </div>
  </nav>
</template>
