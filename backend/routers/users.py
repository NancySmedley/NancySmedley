from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user, get_password_hash, verify_password, create_access_token
import models, schemas

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post("/register", response_model=schemas.Token)
def register(user_data: schemas.UserRegister, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.username == user_data.username).first():
        raise HTTPException(status_code=400, detail="用户名已存在")
    if db.query(models.User).filter(models.User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="邮箱已被注册")

    user = models.User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        phone=user_data.phone,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer", "user": {
        "id": user.id, "username": user.username, "email": user.email, "role": user.role
    }}


@router.post("/login", response_model=schemas.Token)
def login(credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == credentials.username).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="账号已被禁用")

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer", "user": {
        "id": user.id, "username": user.username, "email": user.email,
        "role": user.role, "avatar": user.avatar, "phone": user.phone
    }}


@router.get("/me", response_model=schemas.UserBase)
def get_me(current_user: models.User = Depends(get_current_user)):
    return current_user


@router.put("/me")
def update_me(
    update_data: schemas.UserUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    for key, val in update_data.model_dump(exclude_none=True).items():
        setattr(current_user, key, val)
    db.commit()
    db.refresh(current_user)
    return {"message": "更新成功"}


@router.put("/change-password")
def change_password(
    data: dict,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not verify_password(data.get("old_password", ""), current_user.hashed_password):
        raise HTTPException(status_code=400, detail="原密码错误")
    current_user.hashed_password = get_password_hash(data["new_password"])
    db.commit()
    return {"message": "密码修改成功"}


# --- Addresses ---
@router.get("/addresses")
def get_addresses(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(models.Address).filter(models.Address.user_id == current_user.id).all()


@router.post("/addresses", response_model=schemas.AddressOut)
def create_address(
    address: schemas.AddressCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if address.is_default:
        db.query(models.Address).filter(
            models.Address.user_id == current_user.id
        ).update({"is_default": False})

    db_address = models.Address(user_id=current_user.id, **address.model_dump())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address


@router.put("/addresses/{address_id}", response_model=schemas.AddressOut)
def update_address(
    address_id: int,
    address: schemas.AddressCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_address = db.query(models.Address).filter(
        models.Address.id == address_id, models.Address.user_id == current_user.id
    ).first()
    if not db_address:
        raise HTTPException(status_code=404, detail="地址不存在")

    if address.is_default:
        db.query(models.Address).filter(
            models.Address.user_id == current_user.id
        ).update({"is_default": False})

    for key, val in address.model_dump().items():
        setattr(db_address, key, val)
    db.commit()
    db.refresh(db_address)
    return db_address


@router.delete("/addresses/{address_id}")
def delete_address(
    address_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_address = db.query(models.Address).filter(
        models.Address.id == address_id, models.Address.user_id == current_user.id
    ).first()
    if not db_address:
        raise HTTPException(status_code=404, detail="地址不存在")
    db.delete(db_address)
    db.commit()
    return {"message": "删除成功"}
