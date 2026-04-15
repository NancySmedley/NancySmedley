from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from database import engine
import models
from routers import users, products, cart, orders, admin
from seed import init_db

# 创建数据表并初始化数据
models.Base.metadata.create_all(bind=engine)
init_db()

app = FastAPI(
    title="iKF 音频产品商城 API",
    description="类似 iKF 的音频产品电商网站后端 API",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静态文件（上传的图片）
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# 路由
app.include_router(users.router)
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(orders.router)
app.include_router(admin.router)


@app.get("/")
def root():
    return {"message": "iKF Store API", "docs": "/docs"}
