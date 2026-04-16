from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# --- Auth ---
class UserRegister(BaseModel):
    username: str
    email: str
    password: str
    phone: Optional[str] = None


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    user: dict


# --- User ---
class UserBase(BaseModel):
    id: int
    username: str
    email: str
    phone: Optional[str] = None
    avatar: Optional[str] = None
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    phone: Optional[str] = None
    avatar: Optional[str] = None


# --- Category ---
class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None
    sort_order: int = 0


class CategoryOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None
    sort_order: int
    is_active: bool

    class Config:
        from_attributes = True


# --- Product ---
class ProductCreate(BaseModel):
    name: str
    short_desc: Optional[str] = None
    description: Optional[str] = None
    cover_image: Optional[str] = None
    images: Optional[str] = None
    colors: Optional[str] = None
    specs: Optional[str] = None
    external_link: Optional[str] = None
    series: Optional[str] = None
    category_id: Optional[int] = None
    is_featured: bool = False
    is_lifestyle: bool = False
    is_fashion: bool = False
    sort_order: int = 0


class ProductUpdate(ProductCreate):
    pass


class ProductOut(BaseModel):
    id: int
    name: str
    short_desc: Optional[str] = None
    description: Optional[str] = None
    cover_image: Optional[str] = None
    images: Optional[str] = None
    colors: Optional[str] = None
    specs: Optional[str] = None
    external_link: Optional[str] = None
    series: Optional[str] = None
    category_id: Optional[int] = None
    is_active: bool
    is_featured: bool
    is_lifestyle: bool
    is_fashion: bool
    sort_order: int
    created_at: datetime
    category: Optional[CategoryOut] = None

    class Config:
        from_attributes = True


# --- Banner ---
class BannerCreate(BaseModel):
    title: Optional[str] = None
    subtitle: Optional[str] = None
    features: Optional[str] = None
    image: str
    bg_color: str = "#1a1a2e"
    btn_text: str = "立即购买"
    link: Optional[str] = None
    sort_order: int = 0


class BannerOut(BaseModel):
    id: int
    title: Optional[str] = None
    subtitle: Optional[str] = None
    features: Optional[str] = None
    image: str
    bg_color: str
    btn_text: str
    link: Optional[str] = None
    sort_order: int
    is_active: bool

    class Config:
        from_attributes = True


# --- Download ---
class DownloadCreate(BaseModel):
    name: str
    description: Optional[str] = None
    version: Optional[str] = None
    cover_image: Optional[str] = None
    ios_url: Optional[str] = None
    android_url: Optional[str] = None
    windows_url: Optional[str] = None
    mac_url: Optional[str] = None
    sort_order: int = 0


class DownloadOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    version: Optional[str] = None
    cover_image: Optional[str] = None
    ios_url: Optional[str] = None
    android_url: Optional[str] = None
    windows_url: Optional[str] = None
    mac_url: Optional[str] = None
    sort_order: int
    is_active: bool

    class Config:
        from_attributes = True


# --- Manual ---
class ManualCreate(BaseModel):
    product_name: str
    cover_image: Optional[str] = None
    file_url: Optional[str] = None
    description: Optional[str] = None
    sort_order: int = 0


class ManualOut(BaseModel):
    id: int
    product_name: str
    cover_image: Optional[str] = None
    file_url: Optional[str] = None
    description: Optional[str] = None
    sort_order: int
    is_active: bool

    class Config:
        from_attributes = True


# --- PageContent ---
class PageContentCreate(BaseModel):
    page_key: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None
    images: Optional[str] = None


class PageContentOut(BaseModel):
    id: int
    page_key: str
    title: Optional[str] = None
    content: Optional[str] = None
    images: Optional[str] = None

    class Config:
        from_attributes = True


# --- Dashboard Stats ---
class DashboardStats(BaseModel):
    total_products: int
    total_downloads: int
    total_manuals: int
    total_users: int
