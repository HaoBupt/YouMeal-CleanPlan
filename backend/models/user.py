# models/user.py
"""
用户模型 - 最基础版本
只包含最核心的数据库操作
"""

from app import db
from datetime import datetime

class User(db.Model):
    """用户表"""
    
    # 表名
    __tablename__ = 'users'
    
    # ========== 最基本的字段 ==========
    
    # 主键
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='用户ID')
    
    # 学号（唯一标识）
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    
    # 手机号（可选）
    phone = db.Column(db.String(20))
    
    # 邮箱（可选）
    email = db.Column(db.String(120))
    
    # 创建时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # ========== 最基本的方法 ==========
    
    def __init__(self, student_id, phone=None, email=None):
        """初始化用户"""
        self.student_id = student_id
        self.phone = phone
        self.email = email
    
    def to_dict(self):
        """转换为字典（用于API返回）"""
        return {
            'id': self.id,
            'student_id': self.student_id,
            'phone': self.phone,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @classmethod
    def find_by_student_id(cls, student_id):
        """根据学号查找用户"""
        return cls.query.filter_by(student_id=student_id).first()
    
    def save(self):
        """保存到数据库"""
        db.session.add(self)
        db.session.commit()
        return self
    
    def delete(self):
        """从数据库删除"""
        db.session.delete(self)
        db.session.commit()
        return True
    
    # ========== 魔术方法（用于调试） ==========
    
    def __repr__(self):
        """调试时显示的信息"""
        return f'<User {self.student_id}>'
    
    def __str__(self):
        """转换为字符串"""
        return f'用户: {self.student_id}'