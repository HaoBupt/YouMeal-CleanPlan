#!/bin/bash
# 一键安装脚本

echo "安装 '邮'你清盘 后端环境..."

# 1. 更新系统
sudo apt update
sudo apt upgrade -y

# 2. 安装基础依赖
sudo apt install -y python3-pip python3-venv python3-dev sqlite3

# 3. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 4. 安装Python依赖
pip install --upgrade pip
pip install -r requirements.txt

# 5. 初始化数据库
mkdir -p instance uploads logs
export FLASK_APP=app.py
flask init-db

# 6. 设置脚本权限
chmod +x scripts/*.sh

echo "安装完成！"
echo "启动开发服务器: ./scripts/start_dev.sh"