#!/bin/bash
# 生产环境启动脚本

set -e

# 激活虚拟环境
source venv/bin/activate

# 生产环境配置
export FLASK_APP=app.py
export FLASK_ENV=production
export FLASK_CONFIG=production
export SECRET_KEY=$(openssl rand -hex 32)
export JWT_SECRET_KEY=$(openssl rand -hex 32)

# 使用gunicorn启动
gunicorn --bind 0.0.0.0:5000 \
         --workers 4 \
         --threads 2 \
         --timeout 120 \
         --access-logfile logs/access.log \
         --error-logfile logs/error.log \
         --log-level info \
         --capture-output \
         --enable-stdio-inheritance \
         "app:create_app()"