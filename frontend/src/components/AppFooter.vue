<template>
  <footer class="footer">
    <div class="container">
      <div class="footer-inner">
        <div class="footer-brand">
          <div class="footer-logo">
            <div class="logo-circle">✦</div>
            <span>ShineSphere</span>
          </div>
          <div style="font-size:12px;color:#999;margin-bottom:16px">绚映星球</div>
          <div class="footer-socials">
            <div class="social-icon" title="抖音">d</div>
            <div class="social-icon" title="微博">微</div>
            <div class="social-icon" title="小红书">红</div>
            <div class="social-icon" title="哔哩哔哩">B</div>
          </div>
        </div>

        <div class="footer-col">
          <h4>产品</h4>
          <ul>
            <li @click="$router.push('/ai-headphones?series=复古系列')">复古系列</li>
            <li @click="$router.push('/ai-headphones?series=开放式系列')">开放式系列</li>
            <li @click="$router.push('/ai-headphones?series=蓝牙系列')">蓝牙系列</li>
            <li @click="$router.push('/ai-headphones?series=睡眠&运动系列')">睡眠&运动系列</li>
            <li @click="$router.push('/ai-headphones?series=头戴系列')">头戴系列</li>
            <li @click="$router.push('/ai-headphones?series=游戏电竞系列')">游戏电竞系列</li>
          </ul>
        </div>

        <div class="footer-col footer-contact">
          <h4>联系我们</h4>
          <p>📞 服务热线：400-0000-000</p>
          <p>💼 团购热线：请联系客服</p>
          <p>✉️ 企业邮箱：contact@shinesphere.com</p>
          <p>🕐 服务时间：周一至周日 9:00-18:00</p>
        </div>

        <div class="footer-qrcodes">
          <div class="qr-item">
            <div style="width:80px;height:80px;background:#f0f0f0;border:1px solid #ddd;display:flex;align-items:center;justify-content:center;font-size:24px">📱</div>
            <p>扫码下载<br>ShineSphere App</p>
          </div>
          <div class="qr-item">
            <div style="width:80px;height:80px;background:#f0f0f0;border:1px solid #ddd;display:flex;align-items:center;justify-content:center;font-size:24px">💬</div>
            <p>扫码关注<br>官方公众号</p>
          </div>
          <div class="qr-item">
            <div style="width:80px;height:80px;background:#f0f0f0;border:1px solid #ddd;display:flex;align-items:center;justify-content:center;font-size:24px">🤝</div>
            <p>扫码添加<br>商务微信</p>
          </div>
        </div>
      </div>

      <div class="footer-bottom">
        Copyright 2024-2025 绚映星球 ShineSphere. All Rights Reserved.
      </div>
    </div>
  </footer>
</template>
