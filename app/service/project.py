import re
from datetime import datetime

from sqlalchemy import or_
from flask import abort

from config import Config
from app.enum import BusiEnum, ResponseEnum
from app.model.project import Project
from app.exception import InvalidUsage, SvnOperateException
from app.extensions import create_repository, save_authz, db, delete_repository


class ProjectService:
    def __init__(self, values):
        self.id = values.get(key='id', type=int, default=None)
        self.name = values.get(key='name', type=str, default=None)
        self.path = values.get(key='path', type=str, default=None)
        self.description = values.get(key='description', type=str, default=None)
        self.visibility = values.get(key='visibility', type=str, default=None)
        self.initDirs = values.get(key='initDirs', type=bool, default=False)
        self.searchValue = values.get(key='searchValue', type=str, default=None)
        self.setting_auth_content = values.get('setting_auth_content', type=str, default=None)

    def validate(self):
        if not self.name:
            raise InvalidUsage(payload=ResponseEnum.PROJECT_NAME_CANNOT_BE_EMPTY)
        if not self.path:
            raise InvalidUsage(payload=ResponseEnum.PROJECT_PATH_CANNOT_BE_EMPTY)
        if not self.visibility:
            self.visibility = 'private'

        if self.name_or_path_conflict():
            raise InvalidUsage(payload=ResponseEnum.NAME_OR_PATH_ALREADY_EXISTS)

        visibility_list = (BusiEnum.get_key(BusiEnum.VISIBILITY_PRIVATE),
                           BusiEnum.get_key(BusiEnum.VISIBILITY_PUBLIC))

        if self.visibility not in visibility_list:
            raise InvalidUsage(payload=ResponseEnum.VISIBILITY_NOT_VALID)

        return self

    def save(self):
        # 创建数据库
        project = Project()
        project.name = self.name
        project.path = self.path
        project.description = self.description
        project.visibility = self.visibility
        project.setting_auth_content = self.generate_setting_auth_content()
        project.final_auth_content = self.generate_final_auth_content()
        project.last_activity_on = datetime.now()
        project.save()
        # 创建仓库
        try:
            create_repository(project)
        except SvnOperateException as e:
            project.delete_self()
            raise InvalidUsage(payload=(e.status, e.output))
        # 修改authz文件
        try:
            save_authz(project)
        except SvnOperateException as e:
            project.delete_self()
            raise InvalidUsage(payload=(e.status, e.output))
        self.add_external_field(project)
        return project.to_json()

    def get_by_id(self, project_id):
        if not project_id:
            raise InvalidUsage(payload=ResponseEnum.INVALID_PARAMS)
        project = Project.query.get(project_id)
        self.add_external_field(project)
        if project:
            return project.to_json()
        else:
            abort(404)

    def update_project(self):
        if not self.id:
            raise InvalidUsage(payload=ResponseEnum.INVALID_PARAMS)
        project = Project.query.get(self.id)
        if not project:
            raise InvalidUsage(status_code=404, payload=ResponseEnum.OBJECT_NOT_FOUNT)
        if project.name == self.name and project.description == self.description:
            return project.to_json()
        project.name = self.name
        project.description = self.description
        project.updated_on = datetime.now()
        project.save()
        self.add_external_field(project)
        return project.to_json()

    def delete_project(self, project_id):
        if not project_id:
            raise InvalidUsage(payload=ResponseEnum.INVALID_PARAMS)
        project = Project.query.get(project_id)
        if not project:
            return 'success'

        try:
            delete_repository(project)
            project.delete_self()
        except SvnOperateException:
            raise InvalidUsage(payload=ResponseEnum.SERVER_ERROR)

        return 'success'

    def search(self):
        if self.searchValue:
            results = Project.query.filter(or_(
                Project.name.like('%' + self.searchValue + '%'),
                Project.path.like('%' + self.searchValue + '%'),
                Project.description.like('%' + self.searchValue + '%')
            )).order_by(Project.last_activity_on.desc()).all()
        else:
            results = Project.query.all()

        for p in results:
            self.add_external_field(p)

        return results

    def name_or_path_conflict(self):
        one = Project.query.filter(or_(
            Project.name == self.name,
            Project.path == self.path
        )).first()

        return True if one else False

    def generate_setting_auth_content(self):
        return '[/]\nlidt3 = rw'

    def generate_final_auth_content(self):
        return self.generate_setting_auth_content()

    def update_project_auth(self, project_id):
        if not project_id or not self.setting_auth_content:
            raise InvalidUsage(payload=ResponseEnum.INVALID_PARAMS)
        auth_list = self.setting_auth_content.replace(' ', '').split('\n')

        resouces = []
        defined_groups = []
        used_groups = []
        developers = []
        for index, auth_line in enumerate(auth_list):
            auth_line = auth_line.replace(' ', '')
            if index == 0 and not auth_line.startswith('['):
                err_msg = '第{0}行有错，未定义资源路径'.format(index + 1)
                raise InvalidUsage(payload=(9000, err_msg))
            elif auth_line.startswith('['):
                if not re.search('^\\[[:|/|\\w]+\\]$', auth_line):
                    err_msg = '第{0}行有错，[]未匹配'.format(index + 1)
                    raise InvalidUsage(payload=(9000, err_msg))
                resouces.append(auth_line)
            elif resouces[-1] == '[groups]' and not auth_line.startswith('['):
                group, user_list = self.handle_group_line(index, auth_line)
                defined_groups.append(group)
                developers.append(user_list)
            else:
                if len(auth_line) == 0:
                    continue
                group, user_list = self.handle_normal_line(index, auth_line)
                if group:
                    used_groups.append(group)
                if user_list:
                    developers.append(user_list)

        used_groups_set = set(used_groups)
        defined_groups_set = set(defined_groups)
        for g in used_groups_set:
            if g not in defined_groups_set:
                err_msg = '错误，组{}未定义'.format(g)
                raise InvalidUsage(payload=(9000, err_msg))

        project = Project.query.get(project_id)
        if not project:
            raise InvalidUsage(ResponseEnum.OBJECT_NOT_FOUNT)

        project.setting_auth_content = self.setting_auth_content
        try:
            save_authz(project)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise InvalidUsage(payload=ResponseEnum.SERVER_ERROR)

        return 'success'

    def handle_group_line(self, index, auth_line):
        if not re.search('^\\w+=(\\w+,)*\\w+$', auth_line):
            err_msg = '第{0}行出错，出现非法字符'.format(index + 1)
            raise InvalidUsage(payload=(9000, err_msg))
        group = auth_line.split('=')[0]
        users = auth_line.split('=')[1]
        user_list = users.split(',')
        return group, user_list

    def handle_normal_line(self, index, auth_line):
        if not re.search('^((@?\\w+)|(\\*))=(r|rw)?$', auth_line):
            err_msg = '第{0}行出错，出现非法字符或权限不符合（r = 只读 rw = 读写 空 = 无权限）'.format(index + 1)
            raise InvalidUsage(payload=(9000, err_msg))
        if auth_line.startswith('@'):
            group = auth_line.split('=')[0].replace('@', '')
            return group, None

        user = auth_line.split('=')[0]
        return None, user

    def add_external_field(self, project):
        if project:
            if not Config.SVN_BASE_URL:
                project.http_url = 'http://svnadmin.example.com/svn/' + project.path
            if Config.SVN_BASE_URL[-1] == '/':
                project.http_url = Config.SVN_BASE_URL + project.path
            else:
                project.http_url = Config.SVN_BASE_URL + '/' + project.path
