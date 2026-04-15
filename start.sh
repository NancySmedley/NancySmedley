#!/bin/bash
# iKF 电商网站启动脚本

echo "🎧 iKF 音频产品电商网站"
echo "=========================="

# 检查并安装后端依赖
if [ ! -d "backend/venv" ]; then
  echo "📦 安装后端依赖..."
  cd backend
  python3 -m venv venv
  ./venv/bin/pip install -r requirements.txt -q
  cd ..
fi

# 检查前端依赖
if [ ! -d "frontend/node_modules" ]; then
  echo "📦 安装前台依赖..."
  cd frontend && npm install -q && cd ..
fi

if [ ! -d "admin/node_modules" ]; then
  echo "📦 安装后台依赖..."
  cd admin && npm install -q && cd ..
fi

echo ""
echo "🚀 启动服务..."

# 启动后端
cd backend
./venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
cd ..

sleep 2

# 启动前台
cd frontend && npm run dev &
FRONTEND_PID=$!
cd ..

# 启动后台管理
cd admin && npm run dev &
ADMIN_PID=$!
cd ..

echo ""
echo "✅ 服务启动成功！"
echo "================================"
echo "  前台网站:    http://localhost:5173"
echo "  后台管理:    http://localhost:5174/admin"
echo "  API 文档:   http://localhost:8000/docs"
echo "================================"
echo "  管理员账号:  admin"
echo "  管理员密码:  admin123456"
echo "================================"
echo ""
echo "按 Ctrl+C 停止所有服务"

trap "kill $BACKEND_PID $FRONTEND_PID $ADMIN_PID 2>/dev/null; exit" INT TERM
wait
