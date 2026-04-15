from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from database import get_db
import models, schemas

router = APIRouter(prefix="/api/products", tags=["products"])


@router.get("")
def list_products(
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=100),
    category_id: Optional[int] = None,
    keyword: Optional[str] = None,
    featured: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Product).filter(models.Product.is_active == True)

    if category_id:
        query = query.filter(models.Product.category_id == category_id)
    if keyword:
        query = query.filter(models.Product.name.contains(keyword))
    if featured is not None:
        query = query.filter(models.Product.is_featured == featured)

    total = query.count()
    products = query.order_by(models.Product.sort_order.desc(), models.Product.created_at.desc()) \
                    .offset((page - 1) * page_size).limit(page_size).all()

    return {"total": total, "page": page, "page_size": page_size, "items": products}


@router.get("/{product_id}", response_model=schemas.ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(
        models.Product.id == product_id,
        models.Product.is_active == True
    ).first()
    if not product:
        raise HTTPException(status_code=404, detail="产品不存在")
    return product


@router.get("/category/all")
def get_categories(db: Session = Depends(get_db)):
    return db.query(models.Category).filter(
        models.Category.is_active == True
    ).order_by(models.Category.sort_order).all()


@router.get("/banners/all")
def get_banners(db: Session = Depends(get_db)):
    return db.query(models.Banner).filter(
        models.Banner.is_active == True
    ).order_by(models.Banner.sort_order).all()
