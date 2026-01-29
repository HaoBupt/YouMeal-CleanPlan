from .default import DefaultConfig

class DevelopmentConfig(DefaultConfig):
    """开发环境配置"""
    
    DEBUG = True
    TESTING = False
    
    # 开发环境允许所有来源
    CORS_ORIGINS = [
        'http://localhost:3000',
        'http://localhost:5173',
        'http://127.0.0.1:3000',
        'http://127.0.0.1:5173',
    ]
    
    # 开发环境显示SQL语句
    SQLALCHEMY_ECHO = True
    
    # 开发环境日志
    LOG_LEVEL = 'DEBUG'
    
    # 开发环境使用内存数据库或本地SQLite
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'