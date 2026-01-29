#!/bin/bash
# 开发环境启动脚本

set -e  # 遇到错误时退出

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}  '邮'你清盘 - 后端开发服务器${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 激活虚拟环境
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo -e "${GREEN}✓ 虚拟环境已激活${NC}"
else
    echo -e "${BLUE}⚠  创建虚拟环境...${NC}"
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    pip install -r requirements-dev.txt
fi

# 设置环境变量
export FLASK_APP=app.py
export FLASK_ENV=development
export FLASK_CONFIG=development
export SECRET_KEY="dev-secret-$(date +%s)"
export JWT_SECRET_KEY="dev-jwt-$(date +%s)"
export DATABASE_URL="sqlite:///$(pwd)/instance/dev.db"

# 创建必要目录
mkdir -p instance logs uploads

# 显示网络信息
echo ""
echo -e "${BLUE}[网络信息]${NC}"
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo -e "  本地地址: ${GREEN}http://localhost:5000${NC}"
echo -e "  内网地址: ${GREEN}http://$IP_ADDRESS:5000${NC}"
echo -e "  健康检查: ${GREEN}http://$IP_ADDRESS:5000/health${NC}"

# 显示API文档地址
echo -e "  API文档: ${GREEN}http://localhost:5000/apidocs${NC}"

# 启动服务器
echo ""
echo -e "${BLUE}[启动服务器]${NC}"
python app.py