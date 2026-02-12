from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
test_user_counter=0

# ========== 配置JSON返回中文 ==========
app.json.ensure_ascii = False 

# ========== 数据库配置 ==========
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///youmeal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ========== 创建数据库对象 ==========
db = SQLAlchemy(app)

# ========== 初始化用户模型 ==========
# 注意：必须在导入模型后，使用前调用 init_db
from models.user import User
User.init_db(db)  # 关键：将db实例传递给User类

#===========注册蓝图==============
from routes.user_routes import user_bp

app.register_blueprint(user_bp)


# ========== 路由定义 ==========
@app.route('/')
def hello():
    return jsonify({'message': 'YouMeal后端服务启动成功!'})

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

# ========== 测试API ==========
@app.route('/api/test/create-user')
def create_incremental_user():
    """创建递增测试用户"""
    global test_user_counter

    try:
        if test_user_counter == 0:
            all_users = User.get_all()
            for user in all_users:
                if hasattr(user, 'student_id') and user.student_id.startswith('test_'):
                    try:
                        num = int(user.student_id.split('_')[1])
                        if num > test_user_counter:
                            test_user_counter = num
                    except:
                        continue
        
        test_user_counter += 1
        next_id = f'test_{test_user_counter:03d}'

        user = User.create(
            student_id=next_id,
            phone=f'1{test_user_counter % 10}{test_user_counter:09d}',
            email=f'increment{test_user_counter:03d}@test.com'
        )

        return jsonify({
            'status':'success',
            'message':f'递增用户创建成功({next_id})',
            'user':user.to_dict(),
            'counter':test_user_counter,
            'next_id':f'test_{(test_user_counter + 1):03d}'
        })
    except Exception as e:
        test_user_counter += 1
        return jsonify({
            'status':'retry',
            'message':f'创建失败，已自动递增到 test_{test_user_counter:03d}',
            'error':str(e),
            'suggesion':'请重试或访问 api/test/reset-counter 重置'
        }), 500
    
@app.route('/api/test/reset-counter')
def reset_counter():

    global test_user_counter
    all_users = User.get_all()
    max_num = 0
    for user in all_users :
        if hasattr(user, 'student_id') and user.student_id.startswith('test_'):
            try:
                num = int(user.student_id.split('_')[1])
                if num > max_num:
                    max_num = num
            except:
                continue
    
    test_user_counter = max_num

    return jsonify({
        'status':'success',
        'message':f'计数器已重置为 {max_num}',
        'next_id':f'test_{max_num+1:03d}',
        'existing_test_users':max_num
    })


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
                student_id='2025211497',
                phone='13107580661',
                email='2025211497@bupt.cn'
            )
            print("👤 已创建默认测试用户: 2025211497")
    
    # 显示可用API
    print("\n🌐 可用API端点:")
    print("  GET  /                    - 首页")
    print("  GET  /health              - 健康检查")
    print("  GET  /api/test/create-user - 创建测试用户")
    print("  GET  /api/test/list-users  - 列出所有用户")
    print("  GET  /api/test/reset-counter  - 重置测试用户计数器")
    print("  GET  /api/test/find-user/<学号> - 查找用户")
    
    print("\n🚀 启动服务器...")
    app.run(debug=True, host='0.0.0.0', port=5000)