from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# ========== 数据库配置 ==========
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///youmeal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ========== 创建数据库对象 ==========
db = SQLAlchemy(app)

# ========== 初始化用户模型 ==========
# 注意：必须在导入模型后，使用前调用 init_db
from models.user import User
User.init_db(db)  # 关键：将db实例传递给User类

# ========== 路由定义 ==========
@app.route('/')
def hello():
    return jsonify({'message': 'YouMeal后端服务启动成功!'})

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

# ========== 测试API ==========
@app.route('/api/test/create-user')
def test_create_user():
    """测试创建用户"""
    try:
        numbers
        # 使用User.create方法
        user = User.create(
            student_id='test_001',
            phone='12345678901',
            email='test@example.com'
        )
        
        return jsonify({
            'status': 'success',
            'message': '用户创建成功',
            'user': user.to_dict()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/test/list-users')
def test_list_users():
    """测试列出所有用户"""
    try:
        users = User.get_all()
        
        return jsonify({
            'status': 'success',
            'count': len(users),
            'users': [user.to_dict() for user in users]
        })
    except Exception as e:
        return jsonify({
            'status': 'error', 
            'message': str(e)
        }), 500

@app.route('/api/test/find-user/<student_id>')
def test_find_user(student_id):
    """测试查找用户"""
    try:
        user = User.find_by_student_id(student_id)
        
        if user:
            return jsonify({
                'status': 'success',
                'user': user.to_dict()
            })
        else:
            return jsonify({
                'status': 'not_found',
                'message': f'用户 {student_id} 不存在'
            }), 404
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# ========== 应用启动 ==========
if __name__ == '__main__':
    with app.app_context():
        # 创建数据库表
        db.create_all()
        print("✅ 数据库表创建成功")
        
        # 测试用户数量
        user_count = User.count()
        print(f"📊 当前用户数: {user_count}")
        
        # 如果没有用户，创建一个默认的
        if user_count == 0:
            User.create(
                student_id='2025212865',
                phone='13107580661',
                email='2025212865@bupt.cn'
            )
            print("👤 已创建默认测试用户: 2025212865")
    
    # 显示可用API
    print("\n🌐 可用API端点:")
    print("  GET  /                    - 首页")
    print("  GET  /health              - 健康检查")
    print("  GET  /api/test/create-user - 创建测试用户")
    print("  GET  /api/test/list-users  - 列出所有用户")
    print("  GET  /api/test/find-user/<学号> - 查找用户")
    
    print("\n🚀 启动服务器...")
    app.run(debug=True, host='0.0.0.0', port=5000)