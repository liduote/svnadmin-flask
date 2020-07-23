import json
import hashlib
import re
from datetime import datetime

from flask_jwt_extended import get_jwt_claims
from sqlalchemy import or_

from app.enum import ResponseEnum, BusiEnum
from app.model import User
from app.exception import InvalidUsage
from app.extensions import AlchemyEncoder


class UserService:
    def __init__(self, request):
        self.id = request.values.get(key='id', type=int, default=None)
        self.username = request.values.get(key='username', type=str, default=None)
        self.fullname = request.values.get(key='fullname', type=str, default=None)
        self.email = request.values.get(key='email', type=str, default=None)
        self.password = request.values.get(key='password', type=str, default=None)
        self.project_limits = request.values.get(key='project_limits', type=int, default=10)
        self.admin = request.values.get(key='admin', type=int, default=0)
        self.current_user = json.loads(get_jwt_claims())
        self.json_users = request.json

    def validate(self):
        if not self.fullname or not self.username or not self.email:
            raise InvalidUsage(payload=ResponseEnum.ACCOUNT_INFO_CANNOT_BE_EMPTY)
        if not self.password:
            raise InvalidUsage(payload=ResponseEnum.PASSWORD_CANNOT_BE_EMPTY)

        user = User.query.filter(or_(
            User.username == self.username,
            User.email == self.email
        )).first()

        if user and user.username == self.username:
            raise InvalidUsage(payload=ResponseEnum.ACCOUNT_CONFLICT)

        if user and user.email == self.email:
            raise InvalidUsage(payload=ResponseEnum.EMAIL_CONFLICT)

        if self.current_user.get('admin') != 1:
            raise InvalidUsage(payload=ResponseEnum.PERMISSION_ERROR)

        if not re.match(r'[a-z][a-z0-9]+', self.username):
            raise InvalidUsage(payload=ResponseEnum.USERNAME_INVALID)

        if not re.match(r'([a-zA-Z]|[0-9])(\w|-)+@[a-zA-Z0-9]+\.([a-zA-Z]{2,4})', self.email):
            raise InvalidUsage(payload=ResponseEnum.EMAIL_INVALID)

        return self

    def save(self):
        # 创建数据库
        user = User()
        user.username = self.username
        user.password = hashlib.md5(self.password.encode(encoding='utf-8')).hexdigest()
        user.fullname = self.fullname
        user.email = self.email
        user.project_limits = self.project_limits
        user.state = BusiEnum.get_key(BusiEnum.USER_STATE_ACTIVE)
        user.admin = self.admin
        user.created_on = datetime.now()
        user.created_by = self.current_user.get('id')
        user.save()
        return user.to_json()

    def update_users(self):
        if type(self.json_users) is list:
            results = []
            for u in self.json_users:
                user = User.query.get(u.get('id'))
                user.fullname = u.get('fullname')
                user.project_limits = u.get('project_limits')
                user.state = u.get('state')
                user.admin = u.get('admin')
                user.updated_on = datetime.now()
                user.save()
                results.append(user)

            return json.dumps(results, cls=AlchemyEncoder)
        elif type(self.json_users) is dict:
            user = User.query.get(self.json_users.get('id'))
            user.fullname = self.json_users.get('fullname')
            user.project_limits = self.json_users.get('project_limits')
            user.state = self.json_users.get('state')
            user.admin = self.json_users.get('admin')
            user.updated_on = datetime.now()
            user.save()

            return user.to_json()

    def delete_users(self):
        if type(self.json_users) is list:
            for u in self.json_users:
                User.query.get(u.get('id')).delete_self()
        elif type(self.json_users) is dict:
            User.query.get(self.json_users.get('id')).delete_self()

        return 'ok'
