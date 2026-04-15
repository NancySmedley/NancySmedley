from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# --- Auth ---
class UserRegister(BaseModel):
    username: str
    email: EmailStr
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
    phone: Optional[str]
    avatar: Optional[str]
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
    description: Optional[str]
    icon: Optional[str]
    sort_order: int
    is_active: bool

    class Config:
        from_attributes = True


# --- Product ---
class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    original_price: Optional[float] = None
    stock: int = 0
    cover_image: Optional[str] = None
    images: Optional[str] = None
    specs: Optional[str] = None
    category_id: Optional[int] = None
    is_featured: bool = False
    sort_order: int = 0


class ProductUpdate(ProductCreate):
    pass


class ProductOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    original_price: Optional[float]
    stock: int
    sales: int
    cover_image: Optional[str]
    images: Optional[str]
    specs: Optional[str]
    category_id: Optional[int]
    is_active: bool
    is_featured: bool
    sort_order: int
    created_at: datetime
    category: Optional[CategoryOut]

    class Config:
        from_attributes = True


# --- Cart ---
class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = 1


class CartItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    product: ProductOut

    class Config:
        from_attributes = True


# --- Address ---
class AddressCreate(BaseModel):
    name: str
    phone: str
    province: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    detail: str
    is_default: bool = False


class AddressOut(BaseModel):
    id: int
    name: str
    phone: str
    province: Optional[str]
    city: Optional[str]
    district: Optional[str]
    detail: str
    is_default: bool

    class Config:
        from_attributes = True


# --- Order ---
class OrderCreate(BaseModel):
    address_id: int
    remark: Optional[str] = None
    items: List[dict]  # [{product_id, quantity}]


class OrderItemOut(BaseModel):
    id: int
    product_id: int
    product_name: str
    product_image: Optional[str]
    price: float
    quantity: int

    class Config:
        from_attributes = True


class OrderOut(BaseModel):
    id: int
    order_no: str
    total_amount: float
    status: str
    remark: Optional[str]
    created_at: datetime
    items: List[OrderItemOut]
    address: Optional[AddressOut]

    class Config:
        from_attributes = True


# --- Banner ---
class BannerCreate(BaseModel):
    title: Optional[str] = None
    image: str
    link: Optional[str] = None
    sort_order: int = 0


class BannerOut(BaseModel):
    id: int
    title: Optional[str]
    image: str
    link: Optional[str]
    sort_order: int
    is_active: bool

    class Config:
        from_attributes = True


# --- Stats ---
class DashboardStats(BaseModel):
    total_users: int
    total_products: int
    total_orders: int
    total_revenue: float
    recent_orders: List[dict]
