<template>
  <footer class="footer">
    <div class="container">
      <div class="footer-grid">
        <div>
          <div class="footer-brand">i<span>K</span>F</div>
          <p style="font-size:13px;line-height:1.8">只做有趣的音乐产品<br>用先锋设计与前沿科技<br>点燃对音乐的热爱</p>
          <div style="margin-top:16px;display:flex;gap:12px">
            <el-icon size="20" style="cursor:pointer;opacity:0.7"><Platform /></el-icon>
            <el-icon size="20" style="cursor:pointer;opacity:0.7"><ChatDotRound /></el-icon>
            <el-icon size="20" style="cursor:pointer;opacity:0.7"><Phone /></el-icon>
          </div>
        </div>
        <div>
          <h4>产品系列</h4>
          <ul>
            <li><router-link to="/products?category=1">真无线耳机</router-link></li>
            <li><router-link to="/products?category=2">头戴式耳机</router-link></li>
            <li><router-link to="/products?category=3">有线耳机</router-link></li>
            <li><router-link to="/products?category=4">降噪耳机</router-link></li>
          </ul>
        </div>
        <div>
          <h4>服务支持</h4>
          <ul>
            <li><a href="#">常见问题</a></li>
            <li><a href="#">维修政策</a></li>
            <li><a href="#">驱动下载</a></li>
            <li><a href="#">联系客服</a></li>
          </ul>
        </div>
        <div>
          <h4>关于我们</h4>
          <ul>
            <li><a href="#">品牌故事</a></li>
            <li><a href="#">品牌合作</a></li>
            <li><a href="#">用户协议</a></li>
            <li><a href="#">隐私政策</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <p>© 2024 iKF 只做有趣的音乐产品. All Rights Reserved.</p>
      </div>
    </div>
  </footer>
</template>
