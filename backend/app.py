# 替换app.py为以下内容
from flask import Flask, jsonify
import os
from flask_sqlalchemy import SQLAlchemy

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(BASE_DIR, "youmeal.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/')
def hello():
    return jsonify({'message': 'YouMeal后端服务启动成功!'})

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

@app.route('/test/user/count')
def test_count():
    try:
        from models.user import User
        with app.app_context():
            count = db.session.query(User).count()
            return jsonify({"status": "success", "user_count": count})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    print("✅ 数据库表创建成功")   
    app.run(debug=True, host='0.0.0.0', port=5000)