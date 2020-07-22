import json

from flask import request
from sqlalchemy import or_
from flask_jwt_extended import jwt_required

from app.web import main
from app.service import UserService
from app.model import User
from app.extensions import AlchemyEncoder


@main.route('/admin/users', methods=['GET'])
@jwt_required
def get_user_list():
    """
    获取用户列表
    ---
    tags:
      - 用户
    parameters:
      - name: searchKey
        in: query
        type: string
        required: false
    definitions:
      User:
        type: object
        properties:
          id:
            type: integer
          username:
            type: string
          fullname:
            type: string
          email:
            type: string
          sign_in_count:
            type: integer
          project_limits:
            type: integer
          state:
            type: string
          last_activity_on:
            type: string
          admin:
            type: integer
          created_on:
            type: string
          updated_on:
            type: string
          created_by:
            type: integer
    responses:
      200:
        description: 用户列表
        schema:
          $ref: '#/definitions/User'
    """
    search_value = request.values.get('searchKey', None)
    if search_value:
        results = User.query.filter(or_(
            User.username.like('%' + search_value + '%'),
            User.fullname.like('%' + search_value + '%'),
            User.email.like('%' + search_value + '%')
        )).order_by(User.last_activity_on.desc()).all()
    else:
        results = User.query.all()

    return json.dumps(results, cls=AlchemyEncoder)


@main.route('/admin/users', methods=['POST'])
@jwt_required
def create_user():
    """
    创建用户
    ---
    tags:
      - 用户
    parameters:
      - name: username
        in: formData
        type: string
        required: true
      - name: fullname
        in: formData
        type: string
        required: true
      - name: email
        in: formData
        type: string
        required: true
      - name: password
        in: formData
        type: string
        required: true
      - name: project_limits
        in: formData
        type: integer
        required: false
      - name: admin
        in: formData
        type: integer
        required: false
    responses:
      200:
        description: 用户
        schema:
          $ref: '#/definitions/User'
      400:
        description: 创建失败，参数错误
      500:
        description: 创建失败，服务器错误
    """
    return UserService(request).validate().save()


@main.route('/admin/users', methods=['PUT'])
@jwt_required
def update_users():
    return UserService(request).update_users()


@main.route('/admin/users', methods=['DELETE'])
@jwt_required
def delete_users():
    return UserService(request).delete_users()
