# routes/user_routes.py
from flask import Blueprint, jsonify
from models.user import User

user_bp = Blueprint('user', __name__, url_prefix='/api/users')

@user_bp.route('/<student_id>', methods=['DELETE'])
def delete_user_by_student_id(student_id):
    """根据学号删除用户"""
    try:
        success = User.delete_by_student_id(student_id)
        if success:
            return jsonify({
                'code': 200,
                'message': f'用户 {student_id} 删除成功'
            })
        return jsonify({
            'code': 404,
            'error': f'用户 {student_id} 不存在'
        }), 404
    except Exception as e:
        return jsonify({
            'code': 500,
            'error': f'删除失败: {str(e)}'
        }), 500

@user_bp.route('/id/<int:user_id>', methods=['DELETE'])
def delete_user_by_id(user_id):
    """根据用户ID删除用户"""
    try:
        success = User.delete_by_id(user_id)
        if success:
            return jsonify({
                'code': 200,
                'message': f'用户ID {user_id} 删除成功'
            })
        return jsonify({
            'code': 404,
            'error': f'用户ID {user_id} 不存在'
        }), 404
    except Exception as e:
        return jsonify({
            'code': 500,
            'error': f'删除失败: {str(e)}'
        }), 500