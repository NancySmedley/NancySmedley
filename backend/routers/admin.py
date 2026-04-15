from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
import os, uuid, aiofiles
from database import get_db
from auth import get_current_admin
import models, schemas

router = APIRouter(prefix="/api/admin", tags=["admin"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# --- Dashboard ---
@router.get("/stats", response_model=schemas.DashboardStats)
def get_stats(db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    total_users = db.query(models.User).filter(models.User.role == "user").count()
    total_products = db.query(models.Product).count()
    total_orders = db.query(models.Order).count()
    total_revenue = db.query(func.sum(models.Order.total_amount)).filter(
        models.Order.status.in_(["paid", "shipped", "delivered"])
    ).scalar() or 0.0

    recent_orders = db.query(models.Order).order_by(
        models.Order.created_at.desc()
    ).limit(10).all()

    return {
        "total_users": total_users,
        "total_products": total_products,
        "total_orders": total_orders,
        "total_revenue": round(total_revenue, 2),
        "recent_orders": [
            {
                "id": o.id, "order_no": o.order_no,
                "total_amount": o.total_amount, "status": o.status,
                "created_at": o.created_at.isoformat()
            } for o in recent_orders
        ]
    }


# --- File Upload ---
@router.post("/upload")
async def upload_file(file: UploadFile = File(...), admin=Depends(get_current_admin)):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in [".jpg", ".jpeg", ".png", ".gif", ".webp"]:
        raise HTTPException(status_code=400, detail="只支持图片格式")
    filename = f"{uuid.uuid4().hex}{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    async with aiofiles.open(filepath, "wb") as f:
        content = await file.read()
        await f.write(content)
    return {"url": f"/uploads/{filename}"}


# --- Products ---
@router.get("/products")
def admin_list_products(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    keyword: Optional[str] = None,
    category_id: Optional[int] = None,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    query = db.query(models.Product)
    if keyword:
        query = query.filter(models.Product.name.contains(keyword))
    if category_id:
        query = query.filter(models.Product.category_id == category_id)
    total = query.count()
    products = query.order_by(models.Product.created_at.desc()) \
                    .offset((page - 1) * page_size).limit(page_size).all()
    return {"total": total, "items": products}


@router.post("/products", response_model=schemas.ProductOut)
def admin_create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.put("/products/{product_id}", response_model=schemas.ProductOut)
def admin_update_product(
    product_id: int,
    product: schemas.ProductUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="产品不存在")
    for key, val in product.model_dump(exclude_none=True).items():
        setattr(db_product, key, val)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.delete("/products/{product_id}")
def admin_delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="产品不存在")
    db.delete(db_product)
    db.commit()
    return {"message": "删除成功"}


# --- Categories ---
@router.get("/categories")
def admin_list_categories(db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    return db.query(models.Category).order_by(models.Category.sort_order).all()


@router.post("/categories", response_model=schemas.CategoryOut)
def admin_create_category(
    category: schemas.CategoryCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    if db.query(models.Category).filter(models.Category.name == category.name).first():
        raise HTTPException(status_code=400, detail="分类名称已存在")
    db_cat = models.Category(**category.model_dump())
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat


@router.put("/categories/{cat_id}", response_model=schemas.CategoryOut)
def admin_update_category(
    cat_id: int,
    category: schemas.CategoryCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    db_cat = db.query(models.Category).filter(models.Category.id == cat_id).first()
    if not db_cat:
        raise HTTPException(status_code=404, detail="分类不存在")
    for key, val in category.model_dump().items():
        setattr(db_cat, key, val)
    db.commit()
    db.refresh(db_cat)
    return db_cat


@router.delete("/categories/{cat_id}")
def admin_delete_category(
    cat_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    db_cat = db.query(models.Category).filter(models.Category.id == cat_id).first()
    if not db_cat:
        raise HTTPException(status_code=404, detail="分类不存在")
    db.delete(db_cat)
    db.commit()
    return {"message": "删除成功"}


# --- Orders ---
@router.get("/orders")
def admin_list_orders(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    query = db.query(models.Order)
    if status:
        query = query.filter(models.Order.status == status)
    total = query.count()
    orders = query.order_by(models.Order.created_at.desc()) \
                  .offset((page - 1) * page_size).limit(page_size).all()
    return {"total": total, "items": orders}


@router.put("/orders/{order_id}/status")
def admin_update_order_status(
    order_id: int,
    data: dict,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    order.status = data.get("status", order.status)
    db.commit()
    return {"message": "状态更新成功"}


# --- Users ---
@router.get("/users")
def admin_list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    keyword: Optional[str] = None,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    query = db.query(models.User).filter(models.User.role == "user")
    if keyword:
        query = query.filter(
            models.User.username.contains(keyword) | models.User.email.contains(keyword)
        )
    total = query.count()
    users = query.order_by(models.User.created_at.desc()) \
                 .offset((page - 1) * page_size).limit(page_size).all()
    return {"total": total, "items": users}


@router.put("/users/{user_id}/status")
def admin_toggle_user(
    user_id: int,
    data: dict,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    user.is_active = data.get("is_active", user.is_active)
    db.commit()
    return {"message": "用户状态已更新"}


# --- Banners ---
@router.get("/banners")
def admin_list_banners(db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    return db.query(models.Banner).order_by(models.Banner.sort_order).all()


@router.post("/banners", response_model=schemas.BannerOut)
def admin_create_banner(
    banner: schemas.BannerCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    db_banner = models.Banner(**banner.model_dump())
    db.add(db_banner)
    db.commit()
    db.refresh(db_banner)
    return db_banner


@router.put("/banners/{banner_id}", response_model=schemas.BannerOut)
def admin_update_banner(
    banner_id: int,
    banner: schemas.BannerCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    db_banner = db.query(models.Banner).filter(models.Banner.id == banner_id).first()
    if not db_banner:
        raise HTTPException(status_code=404, detail="轮播图不存在")
    for key, val in banner.model_dump().items():
        setattr(db_banner, key, val)
    db.commit()
    db.refresh(db_banner)
    return db_banner


@router.delete("/banners/{banner_id}")
def admin_delete_banner(
    banner_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    db_banner = db.query(models.Banner).filter(models.Banner.id == banner_id).first()
    if not db_banner:
        raise HTTPException(status_code=404, detail="轮播图不存在")
    db.delete(db_banner)
    db.commit()
    return {"message": "删除成功"}
