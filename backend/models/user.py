# models/user.py - 延迟初始化版本
"""
用户模型 - 延迟初始化版本
"""

class User:
    """用户模型类（不直接继承db.Model）"""
    
    # 类属性，稍后设置
    _db = None
    _model = None
    
    @classmethod
    def init_db(cls, db_instance):
        """初始化数据库连接（必须在app启动前调用）"""
        cls._db = db_instance
        
        # 动态创建真正的模型类
        class UserModel(cls._db.Model):
            __tablename__ = 'users'
            
            id = cls._db.Column(cls._db.Integer, primary_key=True)
            student_id = cls._db.Column(cls._db.String(20), unique=True, nullable=False)
            phone = cls._db.Column(cls._db.String(20))
            email = cls._db.Column(cls._db.String(120))
            created_at = cls._db.Column(cls._db.DateTime, default=cls._db.func.now())
            
            def __init__(self, student_id, phone=None, email=None):
                self.student_id = student_id
                self.phone = phone
                self.email = email
            
            def to_dict(self):
                return {
                    'id': self.id,
                    'student_id': self.student_id,
                    'phone': self.phone,
                    'email': self.email,
                    'created_at': self.created_at.isoformat() if self.created_at else None
                }
            
            def save(self):
                cls._db.session.add(self)
                cls._db.session.commit()
                return self
            
            @classmethod
            def find_by_student_id(cls, student_id):
                return cls.query.filter_by(student_id=student_id).first()
            
            def __repr__(self):
                return f'<User {self.student_id}>'
        
        cls._model = UserModel
    
    @classmethod
    def query(cls):
        """查询接口"""
        if not cls._model:
            raise RuntimeError("数据库未初始化，请先调用 User.init_db(db)")
        return cls._model.query
    
    @classmethod
    def create(cls, student_id, phone=None, email=None):
        """创建用户"""
        if not cls._model:
            raise RuntimeError("数据库未初始化")
        
        user = cls._model(
            student_id=student_id,
            phone=phone,
            email=email
        )
        cls._db.session.add(user)
        cls._db.session.commit()
        return user
    
    @classmethod
    def find_by_student_id(cls, student_id):
        """查找用户"""
        if not cls._model:
            return None
        return cls._model.query.filter_by(student_id=student_id).first()
    
    @classmethod
    def get_all(cls):
        """获取所有用户"""
        if not cls._model:
            return []
        return cls._model.query.all()
    
    @classmethod
    def count(cls):
        """获取用户数量"""
        if not cls._model:
            return 0
        return cls._model.query.count()
    
    # 为了方便使用，添加这些别名方法
    @classmethod
    def get(cls, user_id):
        """根据ID获取用户"""
        if not cls._model:
            return None
        return cls._model.query.get(user_id)