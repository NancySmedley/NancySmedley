from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
import models

router = APIRouter(prefix="/api/products", tags=["products"])


@router.get("")
def list_products(
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=100),
    category_id: Optional[int] = None,
    series: Optional[str] = None,
    keyword: Optional[str] = None,
    featured: Optional[bool] = None,
    lifestyle: Optional[bool] = None,
    fashion: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Product).filter(models.Product.is_active == True)
    if category_id:
        query = query.filter(models.Product.category_id == category_id)
    if series:
        query = query.filter(models.Product.series == series)
    if keyword:
        query = query.filter(models.Product.name.contains(keyword))
    if featured is not None:
        query = query.filter(models.Product.is_featured == featured)
    if lifestyle is not None:
        query = query.filter(models.Product.is_lifestyle == lifestyle)
    if fashion is not None:
        query = query.filter(models.Product.is_fashion == fashion)

    total = query.count()
    products = query.order_by(
        models.Product.sort_order.desc(), models.Product.created_at.desc()
    ).offset((page - 1) * page_size).limit(page_size).all()
    return {"total": total, "page": page, "page_size": page_size, "items": products}


@router.get("/series/all")
def get_series(db: Session = Depends(get_db)):
    """获取所有产品系列（用于Tab分类）"""
    result = db.query(models.Product.series).filter(
        models.Product.is_active == True,
        models.Product.series != None,
        models.Product.series != ""
    ).distinct().all()
    return [r[0] for r in result if r[0]]


@router.get("/categories/all")
def get_categories(db: Session = Depends(get_db)):
    return db.query(models.Category).filter(
        models.Category.is_active == True
    ).order_by(models.Category.sort_order).all()


@router.get("/banners/all")
def get_banners(db: Session = Depends(get_db)):
    return db.query(models.Banner).filter(
        models.Banner.is_active == True
    ).order_by(models.Banner.sort_order).all()


@router.get("/downloads/all")
def get_downloads(db: Session = Depends(get_db)):
    return db.query(models.Download).filter(
        models.Download.is_active == True
    ).order_by(models.Download.sort_order).all()


@router.get("/manuals/all")
def get_manuals(db: Session = Depends(get_db)):
    return db.query(models.Manual).filter(
        models.Manual.is_active == True
    ).order_by(models.Manual.sort_order).all()


@router.get("/page/{page_key}")
def get_page_content(page_key: str, db: Session = Depends(get_db)):
    return db.query(models.PageContent).filter(
        models.PageContent.page_key == page_key
    ).first()


@router.get("/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    from fastapi import HTTPException
    product = db.query(models.Product).filter(
        models.Product.id == product_id,
        models.Product.is_active == True
    ).first()
    if not product:
        raise HTTPException(status_code=404, detail="产品不存在")
    return product
