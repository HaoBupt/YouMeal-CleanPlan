import os

def get_config():
    """获取配置类"""
    config_name = os.environ.get('FLASK_CONFIG', 'development')
    
    config_map = {
        'development': 'config.development.DevelopmentConfig',
        'production': 'config.production.ProductionConfig',
        'school': 'config.school.SchoolConfig',
        'default': 'config.default.DefaultConfig',
    }
    
    if config_name in config_map:
        module_name, class_name = config_map[config_name].rsplit('.', 1)
        module = __import__(module_name, fromlist=[class_name])
        return getattr(module, class_name)
    
    # 默认使用开发配置
    from .development import DevelopmentConfig
    return DevelopmentConfig