"""初始化数据库并插入示例数据"""
from database import engine, SessionLocal
import models
from auth import get_password_hash

def init_db():
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # 创建管理员账号
    if not db.query(models.User).filter(models.User.username == "admin").first():
        admin = models.User(
            username="admin",
            email="admin@ikf-store.com",
            hashed_password=get_password_hash("admin123456"),
            role="admin",
            is_active=True
        )
        db.add(admin)

    # 创建示例分类
    categories_data = [
        {"name": "真无线耳机", "description": "TWS 真无线蓝牙耳机", "icon": "🎧", "sort_order": 1},
        {"name": "头戴式耳机", "description": "头戴式高保真耳机", "icon": "🎵", "sort_order": 2},
        {"name": "有线耳机", "description": "有线入耳式耳机", "icon": "🎶", "sort_order": 3},
        {"name": "降噪耳机", "description": "主动降噪耳机", "icon": "🔇", "sort_order": 4},
        {"name": "运动耳机", "description": "专为运动设计的耳机", "icon": "🏃", "sort_order": 5},
    ]

    categories = {}
    for cat_data in categories_data:
        existing = db.query(models.Category).filter(models.Category.name == cat_data["name"]).first()
        if not existing:
            cat = models.Category(**cat_data)
            db.add(cat)
            db.flush()
            categories[cat_data["name"]] = cat.id
        else:
            categories[cat_data["name"]] = existing.id

    # 创建示例产品
    products_data = [
        {
            "name": "iKF Air Pro 真无线降噪耳机",
            "description": "搭载先进主动降噪技术，40dB降噪深度，感受极致沉浸音乐体验。蓝牙5.3芯片，超低延迟连接，双麦克风通话清晰。单次续航8小时，配合充电盒达32小时。",
            "price": 299.00, "original_price": 499.00, "stock": 100, "sales": 256,
            "cover_image": "https://picsum.photos/seed/ikf1/400/400",
            "images": '["https://picsum.photos/seed/ikf1/800/800","https://picsum.photos/seed/ikf1b/800/800"]',
            "specs": '{"连接方式":"蓝牙5.3","频率响应":"20Hz-20kHz","续航":"8+24小时","重量":"5g/单耳","防水等级":"IPX5"}',
            "category_id": categories.get("真无线耳机"), "is_featured": True, "sort_order": 10
        },
        {
            "name": "iKF Beat 头戴式蓝牙耳机",
            "description": "40mm大口径动圈单元，HIFI音质输出。折叠设计便携携带，头梁可调节适配多种头型。支持有线/无线双模式，30小时超长续航。",
            "price": 399.00, "original_price": 599.00, "stock": 50, "sales": 128,
            "cover_image": "https://picsum.photos/seed/ikf2/400/400",
            "images": '["https://picsum.photos/seed/ikf2/800/800"]',
            "specs": '{"单元尺寸":"40mm","频率响应":"20Hz-20kHz","续航":"30小时","重量":"220g","阻抗":"32Ω"}',
            "category_id": categories.get("头戴式耳机"), "is_featured": True, "sort_order": 9
        },
        {
            "name": "iKF Fun 运动防水耳机",
            "description": "专为运动设计，IPX7防水防汗，剧烈运动不脱落。环绕式挂耳设计，稳固贴合。单次续航6小时，充电盒额外提供18小时。",
            "price": 199.00, "original_price": 299.00, "stock": 200, "sales": 512,
            "cover_image": "https://picsum.photos/seed/ikf3/400/400",
            "images": '["https://picsum.photos/seed/ikf3/800/800"]',
            "specs": '{"防水等级":"IPX7","续航":"6+18小时","连接":"蓝牙5.2","重量":"4.5g/单耳"}',
            "category_id": categories.get("运动耳机"), "is_featured": True, "sort_order": 8
        },
        {
            "name": "iKF Star 入耳式有线耳机",
            "description": "专业调音师调校，精准还原音乐细节。人体工学入耳设计，长时间佩戴无压迫感。兼容3.5mm接口，支持安卓/iOS双平台线控。",
            "price": 99.00, "original_price": 159.00, "stock": 300, "sales": 1024,
            "cover_image": "https://picsum.photos/seed/ikf4/400/400",
            "images": '["https://picsum.photos/seed/ikf4/800/800"]',
            "specs": '{"接口":"3.5mm","线长":"1.2m","频率响应":"20Hz-20kHz","灵敏度":"98dB","阻抗":"16Ω"}',
            "category_id": categories.get("有线耳机"), "is_featured": False, "sort_order": 7
        },
        {
            "name": "iKF Noise Pro 主动降噪头戴耳机",
            "description": "业界顶级ANC主动降噪，最高降噪深度45dB。搭载LDAC高清音频编码，无损音质传输。智能透传模式，安全感知周围环境。",
            "price": 699.00, "original_price": 999.00, "stock": 30, "sales": 89,
            "cover_image": "https://picsum.photos/seed/ikf5/400/400",
            "images": '["https://picsum.photos/seed/ikf5/800/800"]',
            "specs": '{"降噪深度":"45dB","编码":"LDAC/AAC/SBC","续航":"35小时","重量":"250g","充电":"USB-C"}',
            "category_id": categories.get("降噪耳机"), "is_featured": True, "sort_order": 6
        },
        {
            "name": "iKF Mini 迷你真无线耳机",
            "description": "超小巧充电盒，口袋轻松放入。单次续航5小时，充电盒提供额外15小时。一键式操控，简单易用。",
            "price": 149.00, "original_price": 199.00, "stock": 150, "sales": 368,
            "cover_image": "https://picsum.photos/seed/ikf6/400/400",
            "images": '["https://picsum.photos/seed/ikf6/800/800"]',
            "specs": '{"续航":"5+15小时","连接":"蓝牙5.0","防水":"IPX4","充电盒重量":"35g"}',
            "category_id": categories.get("真无线耳机"), "is_featured": False, "sort_order": 5
        },
    ]

    for prod_data in products_data:
        if not db.query(models.Product).filter(models.Product.name == prod_data["name"]).first():
            product = models.Product(**prod_data)
            db.add(product)

    # 创建示例轮播图
    banners_data = [
        {"title": "iKF Air Pro 旗舰新品", "image": "https://picsum.photos/seed/banner1/1200/400", "link": "/products", "sort_order": 1},
        {"title": "运动系列全新上市", "image": "https://picsum.photos/seed/banner2/1200/400", "link": "/products", "sort_order": 2},
        {"title": "节日特惠 限时折扣", "image": "https://picsum.photos/seed/banner3/1200/400", "link": "/products", "sort_order": 3},
    ]

    for banner_data in banners_data:
        if not db.query(models.Banner).filter(models.Banner.title == banner_data["title"]).first():
            banner = models.Banner(**banner_data)
            db.add(banner)

    db.commit()
    db.close()
    print("✅ 数据库初始化完成！")
    print("👤 管理员账号: admin / admin123456")


if __name__ == "__main__":
    init_db()
