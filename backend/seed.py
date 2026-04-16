"""初始化数据库并插入示例数据"""
from database import engine, SessionLocal
import models
from auth import get_password_hash


def init_db():
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # 管理员账号
    if not db.query(models.User).filter(models.User.username == "admin").first():
        admin = models.User(
            username="admin", email="admin@shinesphere.com",
            hashed_password=get_password_hash("admin123456"),
            role="admin", is_active=True
        )
        db.add(admin)

    # 产品分类
    cats = [
        {"name": "蓝牙系列", "sort_order": 1},
        {"name": "头戴系列", "sort_order": 2},
        {"name": "开放式系列", "sort_order": 3},
        {"name": "复古系列", "sort_order": 4},
        {"name": "游戏电竞系列", "sort_order": 5},
        {"name": "睡眠&运动系列", "sort_order": 6},
    ]
    for c in cats:
        if not db.query(models.Category).filter(models.Category.name == c["name"]).first():
            db.add(models.Category(**c))
    db.flush()

    # 示例产品
    cat_map = {c.name: c.id for c in db.query(models.Category).all()}
    products = [
        {
            "name": "ShineSphere Pro Max 头戴耳机", "short_desc": "LDAC无损解析 | 宽频智慧降噪 | 40小时续航",
            "cover_image": "https://picsum.photos/seed/ss-promax/600/600",
            "colors": '["#F5F0E8","#2C2C2C","#4A6FA5"]',
            "external_link": "https://www.tmall.com", "series": "头戴系列",
            "category_id": cat_map.get("头戴系列"), "is_featured": True, "sort_order": 10
        },
        {
            "name": "ShineSphere S1 头戴耳机", "short_desc": "40mm大动圈喇叭 | 59小时折叠续航 | Hi-Res认证",
            "cover_image": "https://picsum.photos/seed/ss-s1/600/600",
            "colors": '["#F5F0E8","#8B4513","#000000"]',
            "external_link": "https://www.tmall.com", "series": "头戴系列",
            "category_id": cat_map.get("头戴系列"), "is_featured": True, "sort_order": 9
        },
        {
            "name": "ShineSphere G7 游戏耳机", "short_desc": "高分子螺旋振膜 | 4麦混合降噪 | 7.1环绕声效",
            "cover_image": "https://picsum.photos/seed/ss-g7/600/600",
            "colors": '["#2C2C2C","#4A7C59"]',
            "external_link": "https://www.tmall.com", "series": "游戏电竞系列",
            "category_id": cat_map.get("游戏电竞系列"), "is_featured": True, "sort_order": 8
        },
        {
            "name": "ShineSphere Air 月影", "short_desc": "AI降噪 | 13mm同频全动圈 | LDAC Hi-Res",
            "cover_image": "https://picsum.photos/seed/ss-yuying/600/600",
            "colors": '["#F5F0E8","#C8A882"]',
            "external_link": "https://www.tmall.com", "series": "蓝牙系列",
            "category_id": cat_map.get("蓝牙系列"), "is_lifestyle": True, "sort_order": 7
        },
        {
            "name": "ShineSphere Open Clip 开放式", "short_desc": "12mm大动圈 | 运动防脱落 | 彩陶音质",
            "cover_image": "https://picsum.photos/seed/ss-clip/600/600",
            "colors": '["#F5F0E8","#D4B896"]',
            "external_link": "https://www.tmall.com", "series": "开放式系列",
            "category_id": cat_map.get("开放式系列"), "is_lifestyle": True, "sort_order": 6
        },
        {
            "name": "ShineSphere R1 复古头戴耳机", "short_desc": "复古美学设计 潮流时尚穿搭",
            "cover_image": "https://picsum.photos/seed/ss-r1/400/500",
            "external_link": "https://www.tmall.com", "series": "复古系列",
            "category_id": cat_map.get("复古系列"), "is_fashion": True, "sort_order": 5
        },
        {
            "name": "ShineSphere King 主动降噪耳机", "short_desc": "智能降噪 沉浸式聆听体验",
            "cover_image": "https://picsum.photos/seed/ss-king/400/500",
            "external_link": "https://www.tmall.com", "series": "头戴系列",
            "category_id": cat_map.get("头戴系列"), "is_fashion": True, "sort_order": 4
        },
        {
            "name": "ShineSphere R1 Pop 潮流耳机", "short_desc": "年轻潮流 个性穿搭好搭档",
            "cover_image": "https://picsum.photos/seed/ss-r1pop/400/500",
            "external_link": "https://www.tmall.com", "series": "复古系列",
            "category_id": cat_map.get("复古系列"), "is_fashion": True, "sort_order": 3
        },
    ]
    for p in products:
        if not db.query(models.Product).filter(models.Product.name == p["name"]).first():
            db.add(models.Product(**p))

    # 示例Banner
    banners = [
        {
            "title": "ShineSphere Pro Max 旗舰头戴耳机",
            "subtitle": "职业级降噪 | 无损音质体验",
            "features": '["LDAC无损解析","智能降噪","APP智能管理"]',
            "image": "https://picsum.photos/seed/ss-banner1/1400/560",
            "bg_color": "#1a0a2e",
            "btn_text": "立即购买", "link": "https://www.tmall.com", "sort_order": 1
        },
        {
            "title": "ShineSphere S1 经典头戴",
            "subtitle": "40小时超长续航 折叠便携设计",
            "features": '["40mm大动圈","59小时续航","Hi-Res认证"]',
            "image": "https://picsum.photos/seed/ss-banner2/1400/560",
            "bg_color": "#0a1628",
            "btn_text": "立即购买", "link": "https://www.tmall.com", "sort_order": 2
        },
    ]
    for b in banners:
        if not db.query(models.Banner).filter(models.Banner.title == b["title"]).first():
            db.add(models.Banner(**b))

    # 示例软件下载
    if not db.query(models.Download).first():
        db.add(models.Download(
            name="ShineSphere APP",
            description="耳机弹窗配对 | 电量实时显示 | 自定义功能键 | 游戏低延迟模式 | 音乐均衡器",
            version="V1.0.0",
            cover_image="https://picsum.photos/seed/ss-app/200/200",
            ios_url="https://apps.apple.com",
            android_url="https://www.android.com",
            sort_order=1
        ))

    # 示例页面内容
    pages = [
        {
            "page_key": "brand",
            "title": "品牌文化",
            "content": "<h2>绚映星球 · 智能音频新体验</h2><p>绚映星球（ShineSphere）成立于2020年，专注于智能音频产品的研发与设计。我们相信，好的声音能让生活更美好，好的设计能让产品与人产生情感连接。</p><h2>我们的使命</h2><p>为每一位热爱生活、追求品质的用户，提供兼具颜值与性能的智能耳机产品，让科技触手可及，让音乐无处不在。</p><h2>设计理念</h2><p>ShineSphere的产品设计融合了东方美学与现代科技，每一款产品都经过反复打磨，力求在外观、音质、佩戴舒适度之间找到完美平衡。</p>"
        },
        {
            "page_key": "cooperation",
            "title": "品牌合作",
            "content": "<h2>携手共赢 共创未来</h2><p>绚映星球欢迎各类品牌合作，包括渠道经销、KOL联名、企业定制、媒体合作等多种形式。</p><p>📞 合作热线：400-0000-000</p><p>✉️ 商务邮箱：contact@shinesphere.com</p><p>🕐 服务时间：周一至周日 9:00-18:00</p>"
        },
        {
            "page_key": "about",
            "title": "关于我们",
            "content": "<h2>关于绚映星球</h2><p>绚映星球（ShineSphere）是一家专注于智能音频产品研发、生产与销售的科技公司，公司总部位于中国深圳，拥有完善的研发团队和生产体系。</p><h2>联系方式</h2><p>📞 服务热线：400-0000-000</p><p>✉️ 企业邮箱：contact@shinesphere.com</p><p>🕐 服务时间：周一至周日 9:00-18:00</p>"
        },
    ]
    for p in pages:
        if not db.query(models.PageContent).filter(models.PageContent.page_key == p["page_key"]).first():
            db.add(models.PageContent(**p))

    db.commit()
    db.close()
    print("✅ 数据库初始化完成！")
    print("👤 管理员账号: admin / admin123456")


if __name__ == "__main__":
    init_db()
