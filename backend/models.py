from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(200), nullable=False)
    phone = Column(String(20))
    avatar = Column(String(200))
    role = Column(String(10), default="user")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(200))
    icon = Column(String(100))
    sort_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    short_desc = Column(String(300))          # 短描述，用于首页展示
    description = Column(Text)
    cover_image = Column(String(300))
    images = Column(Text)                     # JSON 图片列表
    colors = Column(String(300))              # JSON 颜色点列表，如 ["#fff","#000"]
    specs = Column(Text)                      # JSON 规格
    external_link = Column(String(500))       # 外部购买链接（天猫/京东）
    series = Column(String(50))              # 系列，如"蓝牙系列"，用于分类Tab
    category_id = Column(Integer, ForeignKey("categories.id"))
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)   # 主销爆款
    is_lifestyle = Column(Boolean, default=False)  # 为运动而生板块
    is_fashion = Column(Boolean, default=False)    # 穿搭好物板块
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    category = relationship("Category", back_populates="products")


class Banner(Base):
    __tablename__ = "banners"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    subtitle = Column(String(200))            # 副标题
    features = Column(String(500))           # 特性列表，JSON
    image = Column(String(300), nullable=False)
    bg_color = Column(String(20), default="#1a1a2e")  # 背景色
    btn_text = Column(String(50), default="立即购买")
    link = Column(String(300))
    sort_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Download(Base):
    """软件下载"""
    __tablename__ = "downloads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)      # 软件名称
    description = Column(Text)
    version = Column(String(50))
    cover_image = Column(String(300))
    ios_url = Column(String(500))
    android_url = Column(String(500))
    windows_url = Column(String(500))
    mac_url = Column(String(500))
    sort_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Manual(Base):
    """产品说明书"""
    __tablename__ = "manuals"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(200), nullable=False)
    cover_image = Column(String(300))
    file_url = Column(String(500))             # PDF 下载链接
    description = Column(String(300))
    sort_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PageContent(Base):
    """页面内容（品牌文化、关于我们等静态页）"""
    __tablename__ = "page_contents"

    id = Column(Integer, primary_key=True, index=True)
    page_key = Column(String(50), unique=True, nullable=False)  # brand / about / cooperation
    title = Column(String(200))
    content = Column(Text)                    # HTML 富文本
    images = Column(Text)                     # JSON 图片列表
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
