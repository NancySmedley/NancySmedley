from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
from typing import Optional
import os, uuid, aiofiles
from database import get_db
from auth import get_current_admin
import models, schemas

router = APIRouter(prefix="/api/admin", tags=["admin"])
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# --- Dashboard ---
@router.get("/stats")
def get_stats(db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    return {
        "total_products": db.query(models.Product).count(),
        "total_downloads": db.query(models.Download).count(),
        "total_manuals": db.query(models.Manual).count(),
        "total_users": db.query(models.User).filter(models.User.role == "user").count(),
    }


# --- Upload ---
@router.post("/upload")
async def upload_file(file: UploadFile = File(...), admin=Depends(get_current_admin)):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in [".jpg", ".jpeg", ".png", ".gif", ".webp", ".pdf"]:
        raise HTTPException(status_code=400, detail="不支持的文件格式")
    filename = f"{uuid.uuid4().hex}{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    async with aiofiles.open(filepath, "wb") as f:
        content = await file.read()
        await f.write(content)
    return {"url": f"/uploads/{filename}"}


# --- Products ---
@router.get("/products")
def admin_list_products(
    page: int = Query(1, ge=1), page_size: int = Query(20),
    keyword: Optional[str] = None, series: Optional[str] = None,
    db: Session = Depends(get_db), admin=Depends(get_current_admin)
):
    query = db.query(models.Product)
    if keyword:
        query = query.filter(models.Product.name.contains(keyword))
    if series:
        query = query.filter(models.Product.series == series)
    total = query.count()
    items = query.order_by(models.Product.created_at.desc()).offset((page-1)*page_size).limit(page_size).all()
    return {"total": total, "items": items}


@router.post("/products", response_model=schemas.ProductOut)
def admin_create_product(product: schemas.ProductCreate, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    db_p = models.Product(**product.model_dump())
    db.add(db_p); db.commit(); db.refresh(db_p)
    return db_p


@router.put("/products/{pid}", response_model=schemas.ProductOut)
def admin_update_product(pid: int, product: schemas.ProductUpdate, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    db_p = db.query(models.Product).filter(models.Product.id == pid).first()
    if not db_p: raise HTTPException(404, "产品不存在")
    for k, v in product.model_dump(exclude_none=True).items():
        setattr(db_p, k, v)
    db.commit(); db.refresh(db_p)
    return db_p


@router.delete("/products/{pid}")
def admin_delete_product(pid: int, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    db_p = db.query(models.Product).filter(models.Product.id == pid).first()
    if not db_p: raise HTTPException(404, "产品不存在")
    db.delete(db_p); db.commit()
    return {"message": "删除成功"}


# --- Categories ---
@router.get("/categories")
def admin_list_categories(db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    return db.query(models.Category).order_by(models.Category.sort_order).all()


@router.post("/categories", response_model=schemas.CategoryOut)
def admin_create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    db_c = models.Category(**category.model_dump())
    db.add(db_c); db.commit(); db.refresh(db_c)
    return db_c


@router.put("/categories/{cid}", response_model=schemas.CategoryOut)
def admin_update_category(cid: int, category: schemas.CategoryCreate, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    db_c = db.query(models.Category).filter(models.Category.id == cid).first()
    if not db_c: raise HTTPException(404, "分类不存在")
    for k, v in category.model_dump().items():
        setattr(db_c, k, v)
    db.commit(); db.refresh(db_c)
    return db_c


@router.delete("/categories/{cid}")
def admin_delete_category(cid: int, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    db_c = db.query(models.Category).filter(models.Category.id == cid).first()
    if not db_c: raise HTTPException(404, "分类不存在")
    db.delete(db_c); db.commit()
    return {"message": "删除成功"}


# --- Banners ---
@router.get("/banners")
def admin_list_banners(db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    return db.query(models.Banner).order_by(models.Banner.sort_order).all()


@router.post("/banners", response_model=schemas.BannerOut)
def admin_create_banner(banner: schemas.BannerCreate, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    db_b = models.Banner(**banner.model_dump())
    db.add(db_b); db.commit(); db.refresh(db_b)
    return db_b


@router.put("/banners/{bid}", response_model=schemas.BannerOut)
def admin_update_banner(bid: int, banner: schemas.BannerCreate, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    db_b = db.query(models.Banner).filter(models.Banner.id == bid).first()
    if not db_b: raise HTTPException(404, "轮播图不存在")
    for k, v in banner.model_dump().items():
        setattr(db_b, k, v)
    db.commit(); db.refresh(db_b)
    return db_b


@router.delete("/banners/{bid}")
def admin_delete_banner(bid: int, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    db_b = db.query(models.Banner).filter(models.Banner.id == bid).first()
    if not db_b: raise HTTPException(404, "轮播图不存在")
    db.delete(db_b); db.commit()
    return {"message": "删除成功"}


# --- Downloads ---
@router.get("/downloads")
def admin_list_downloads(db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    return db.query(models.Download).order_by(models.Download.sort_order).all()


@router.post("/downloads", response_model=schemas.DownloadOut)
def admin_create_download(download: schemas.DownloadCreate, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    db_d = models.Download(**download.model_dump())
    db.add(db_d); db.commit(); db.refresh(db_d)
    return db_d


@router.put("/downloads/{did}", response_model=schemas.DownloadOut)
def admin_update_download(did: int, download: schemas.DownloadCreate, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    db_d = db.query(models.Download).filter(models.Download.id == did).first()
    if not db_d: raise HTTPException(404, "下载项不存在")
    for k, v in download.model_dump().items():
        setattr(db_d, k, v)
    db.commit(); db.refresh(db_d)
    return db_d


@router.delete("/downloads/{did}")
def admin_delete_download(did: int, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    db_d = db.query(models.Download).filter(models.Download.id == did).first()
    if not db_d: raise HTTPException(404, "下载项不存在")
    db.delete(db_d); db.commit()
    return {"message": "删除成功"}


# --- Manuals ---
@router.get("/manuals")
def admin_list_manuals(db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    return db.query(models.Manual).order_by(models.Manual.sort_order).all()


@router.post("/manuals", response_model=schemas.ManualOut)
def admin_create_manual(manual: schemas.ManualCreate, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    db_m = models.Manual(**manual.model_dump())
    db.add(db_m); db.commit(); db.refresh(db_m)
    return db_m


@router.put("/manuals/{mid}", response_model=schemas.ManualOut)
def admin_update_manual(mid: int, manual: schemas.ManualCreate, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    db_m = db.query(models.Manual).filter(models.Manual.id == mid).first()
    if not db_m: raise HTTPException(404, "说明书不存在")
    for k, v in manual.model_dump().items():
        setattr(db_m, k, v)
    db.commit(); db.refresh(db_m)
    return db_m


@router.delete("/manuals/{mid}")
def admin_delete_manual(mid: int, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    db_m = db.query(models.Manual).filter(models.Manual.id == mid).first()
    if not db_m: raise HTTPException(404, "说明书不存在")
    db.delete(db_m); db.commit()
    return {"message": "删除成功"}


# --- Page Content ---
@router.get("/pages")
def admin_list_pages(db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    return db.query(models.PageContent).all()


@router.put("/pages/{page_key}")
def admin_upsert_page(page_key: str, data: schemas.PageContentCreate, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    page = db.query(models.PageContent).filter(models.PageContent.page_key == page_key).first()
    if page:
        page.title = data.title
        page.content = data.content
        page.images = data.images
    else:
        page = models.PageContent(**data.model_dump())
        db.add(page)
    db.commit()
    return {"message": "保存成功"}


# --- Users ---
@router.get("/users")
def admin_list_users(
    page: int = Query(1), page_size: int = Query(20),
    keyword: Optional[str] = None,
    db: Session = Depends(get_db), admin=Depends(get_current_admin)
):
    query = db.query(models.User).filter(models.User.role == "user")
    if keyword:
        query = query.filter(models.User.username.contains(keyword) | models.User.email.contains(keyword))
    total = query.count()
    users = query.order_by(models.User.created_at.desc()).offset((page-1)*page_size).limit(page_size).all()
    return {"total": total, "items": users}


@router.put("/users/{uid}/status")
def admin_toggle_user(uid: int, data: dict, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    user = db.query(models.User).filter(models.User.id == uid).first()
    if not user: raise HTTPException(404, "用户不存在")
    user.is_active = data.get("is_active", user.is_active)
    db.commit()
    return {"message": "更新成功"}
