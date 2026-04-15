from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db
from auth import get_current_user
import models, schemas

router = APIRouter(prefix="/api/orders", tags=["orders"])


def generate_order_no():
    return "IKF" + datetime.now().strftime("%Y%m%d%H%M%S%f")[:18]


@router.post("", response_model=schemas.OrderOut)
def create_order(
    order_data: schemas.OrderCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    address = db.query(models.Address).filter(
        models.Address.id == order_data.address_id,
        models.Address.user_id == current_user.id
    ).first()
    if not address:
        raise HTTPException(status_code=404, detail="收货地址不存在")

    total_amount = 0.0
    order_items_data = []

    for item_data in order_data.items:
        product = db.query(models.Product).filter(
            models.Product.id == item_data["product_id"]
        ).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"产品 {item_data['product_id']} 不存在")
        qty = item_data.get("quantity", 1)
        if product.stock < qty:
            raise HTTPException(status_code=400, detail=f"产品 {product.name} 库存不足")

        total_amount += product.price * qty
        order_items_data.append({"product": product, "quantity": qty})

    order = models.Order(
        order_no=generate_order_no(),
        user_id=current_user.id,
        address_id=order_data.address_id,
        total_amount=round(total_amount, 2),
        status="pending",
        remark=order_data.remark
    )
    db.add(order)
    db.flush()

    for item_data in order_items_data:
        product = item_data["product"]
        qty = item_data["quantity"]
        order_item = models.OrderItem(
            order_id=order.id,
            product_id=product.id,
            product_name=product.name,
            product_image=product.cover_image,
            price=product.price,
            quantity=qty
        )
        db.add(order_item)
        product.stock -= qty
        product.sales += qty

    # Clear cart items for ordered products
    product_ids = [d["product"].id for d in order_items_data]
    db.query(models.CartItem).filter(
        models.CartItem.user_id == current_user.id,
        models.CartItem.product_id.in_(product_ids)
    ).delete(synchronize_session=False)

    db.commit()
    db.refresh(order)
    return order


@router.get("")
def list_orders(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    status: str = None,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(models.Order).filter(models.Order.user_id == current_user.id)
    if status:
        query = query.filter(models.Order.status == status)
    total = query.count()
    orders = query.order_by(models.Order.created_at.desc()) \
                  .offset((page - 1) * page_size).limit(page_size).all()
    return {"total": total, "items": orders}


@router.get("/{order_id}", response_model=schemas.OrderOut)
def get_order(
    order_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    order = db.query(models.Order).filter(
        models.Order.id == order_id, models.Order.user_id == current_user.id
    ).first()
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    return order


@router.put("/{order_id}/cancel")
def cancel_order(
    order_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    order = db.query(models.Order).filter(
        models.Order.id == order_id, models.Order.user_id == current_user.id
    ).first()
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    if order.status != "pending":
        raise HTTPException(status_code=400, detail="只有待支付订单可以取消")

    order.status = "cancelled"
    for item in order.items:
        item.product.stock += item.quantity
        item.product.sales -= item.quantity
    db.commit()
    return {"message": "订单已取消"}
