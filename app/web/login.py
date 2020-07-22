import json
import hashlib
from datetime import datetime

from flask import request
from sqlalchemy import and_
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_claims

from app.exception import InvalidUsage
from app.enum import ResponseEnum
from app.model import User
from . import main


@main.route('/login', methods=['POST'])
def login():
    """
    登录接口
    ---
    tags:
      - 用户登录
    parameters:
      - name: username
        in: formData
        type: string
      - name: password
        in: formData
        type: string
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
      LoginResponse:
        type: object
        properties:
          access_token:
            type: string
          user_info:
            $ref: '#/definitions/User'
    responses:
      200:
        description: 用户信息以及token信息
        schema:
          $ref: '#/definitions/LoginResponse'
    """
    username = request.values.get('username', default=None)
    password = request.values.get('password', default=None)
    if not username or not password:
        raise InvalidUsage(payload=ResponseEnum.MISSING_USERNAME_OR_PASSWORD)
    user = User.query.filter(and_(
        User.username == username,
        User.password == hashlib.md5(password.encode(encoding='utf-8')).hexdigest(),
        User.state == 'active'
    )).first()
    if not user:
        raise InvalidUsage(payload=ResponseEnum.LOGIN_FAILED)

    user.last_activity_on = datetime.now()
    if user.sign_in_count:
        user.sign_in_count = user.sign_in_count + 1
    else:
        user.sign_in_count = 1
    user.save()
    results = {
        'access_token': create_access_token(identity=user.id, user_claims=user.to_json()),
        'user_info': user.to_dict()
    }
    return json.dumps(results)


@main.route('/get_info', methods=['GET'])
@jwt_required
def get_info():
    return get_jwt_claims()


@main.route('/change_pwd', methods=['POST'])
@jwt_required
def change_pwd():
    current_user = json.loads(get_jwt_claims())
    change_uid = request.values.get('userId', default=None)
    old_pwd = request.values.get('oldPassword', default=None)
    new_pwd = request.values.get('newPassword', default=None)
    if not change_uid:
        raise InvalidUsage(payload=ResponseEnum.USER_ID_CANNOT_BE_EMPTY)

    change_user = User.query.get(change_uid)
    if not change_user:
        raise InvalidUsage(payload=ResponseEnum.OBJECT_NOT_FOUNT)

    if current_user.get('admin') != 1 \
            and change_user.id != current_user.get('id'):
        raise InvalidUsage(payload=ResponseEnum.PERMISSION_ERROR)

    old_pwd_encrypt = hashlib.md5(old_pwd.encode(encoding='utf-8')).hexdigest()
    if change_user.password != old_pwd_encrypt:
        raise InvalidUsage(payload=ResponseEnum.OLDPASSWORD_IS_NOT_MATCH)

    if not new_pwd:
        raise InvalidUsage(payload=ResponseEnum.PASSWORD_CANNOT_BE_EMPTY)

    change_user.password = hashlib.md5(new_pwd.encode(encoding='utf-8')).hexdigest()
    change_user.save()
    return 'ok'
