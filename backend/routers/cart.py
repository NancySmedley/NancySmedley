from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user
import models, schemas

router = APIRouter(prefix="/api/cart", tags=["cart"])


@router.get("")
def get_cart(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    items = db.query(models.CartItem).filter(models.CartItem.user_id == current_user.id).all()
    return items


@router.post("")
def add_to_cart(
    item: schemas.CartItemCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    product = db.query(models.Product).filter(
        models.Product.id == item.product_id, models.Product.is_active == True
    ).first()
    if not product:
        raise HTTPException(status_code=404, detail="产品不存在")
    if product.stock < item.quantity:
        raise HTTPException(status_code=400, detail="库存不足")

    existing = db.query(models.CartItem).filter(
        models.CartItem.user_id == current_user.id,
        models.CartItem.product_id == item.product_id
    ).first()

    if existing:
        existing.quantity += item.quantity
        db.commit()
        db.refresh(existing)
        return existing
    else:
        cart_item = models.CartItem(
            user_id=current_user.id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(cart_item)
        db.commit()
        db.refresh(cart_item)
        return cart_item


@router.put("/{item_id}")
def update_cart_item(
    item_id: int,
    data: dict,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = db.query(models.CartItem).filter(
        models.CartItem.id == item_id, models.CartItem.user_id == current_user.id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="购物车项不存在")

    quantity = data.get("quantity", 1)
    if quantity <= 0:
        db.delete(item)
        db.commit()
        return {"message": "已从购物车移除"}

    item.quantity = quantity
    db.commit()
    return {"message": "更新成功"}


@router.delete("/{item_id}")
def remove_from_cart(
    item_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = db.query(models.CartItem).filter(
        models.CartItem.id == item_id, models.CartItem.user_id == current_user.id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="购物车项不存在")
    db.delete(item)
    db.commit()
    return {"message": "已从购物车移除"}


@router.delete("")
def clear_cart(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    db.query(models.CartItem).filter(models.CartItem.user_id == current_user.id).delete()
    db.commit()
    return {"message": "购物车已清空"}
