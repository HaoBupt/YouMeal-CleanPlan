from .default import DefaultConfig
import os

class SchoolConfig(DefaultConfig):
    """学校服务器配置"""
    
    DEBUG = False
    TESTING = False
    
    # 学校服务器特殊路径
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    
    # 学校服务器可能使用绝对路径
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    
    # 学校内网IP段限制
    CORS_ORIGINS = [
        'http://localhost',
        'http://127.0.0.1',
        'http://10.*',        # 校园网10段
        'http://172.16.*',    # 校园网172段
        'http://192.168.*',   # 校园网192段
        'https://*.bupt.edu.cn',
        'https://*.bupt.cn',
    ]
    
    # 学校环境可能需要MySQL
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/youmeal'
    
    # 学校服务器日志配置
    LOG_LEVEL = 'WARNING'
    LOG_FILE = os.path.join(BASE_DIR, 'logs', 'youmeal.log')
    
    # 学校服务器可能使用反向代理
    PREFERRED_URL_SCHEME = 'http'  # 学校可能没有HTTPS
    
    # 学校服务器可能需要设置SERVER_NAME
    # SERVER_NAME = 'youmeal.bupt.edu.cn'