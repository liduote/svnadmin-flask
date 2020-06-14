import re
import json
from flask import request

from . import main
from app.service import ProjectService
from app.extensions import AlchemyEncoder
from app.exception import InvalidUsage
from app.enum import ResponseEnum
from app.model import Project


@main.route('/projects', methods=['GET'])
def get_project_list():
    """
    获取仓库列表
    ---
    parameters:
      - name: searchKey
        in: query
        type: string
        required: false
    responses:
      200:
        description: 仓库列表
        schema:
          $ref: '#/definitions/Project'
    """
    return json.dumps(ProjectService(request.values).search(), cls=AlchemyEncoder)


@main.route('/projects', methods=['POST'])
def create_project():
    """
    创建svn仓库
    ---
    parameters:
      - name: name
        in: formData
        type: string
        required: true
        default: my-repo
      - name: path
        in: formData
        type: string
        required: true
        default: /my-repo
      - name: description
        in: formData
        type: string
        required: false
      - name: visibility
        in: formData
        type: string
        required: true
        default: private
      - name: initDirs
        in: formData
        type: boolean
        required: false
    definitions:
      Project:
        type: object
        properties:
          id:
            type: integer
          name:
            type: string
          path:
            type: string
          description:
            type: string
          namespace_id:
            type: integer
          visibility:
            type: string
          final_auth_content:
            type: string
          setting_auth_content:
            type: string
          last_activity_on:
            type: string
          created_on:
            type: string
          updated_on:
            type: string
          created_by:
            type: integer
    responses:
      200:
        description: 仓库列表
        schema:
          $ref: '#/definitions/Project'
      400:
        description: 创建失败，参数错误
        examples:
          error: {
            code: 9005,
            message: '仓库名不能为空'
          }
      500:
        description: 创建失败，服务器错误
    """
    return ProjectService(request.values).validate().save()


@main.route('/projects/<int:project_id>', methods=['GET'])
def get_project_by_id(project_id):
    """
    根据id获取仓库
    ---
    parameters:
      - name: project_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: 仓库
        schema:
          $ref: '#/definitions/Project'
    """
    return ProjectService(request.values).get_by_id(project_id)


@main.route('/projects', methods=['PUT'])
def update_project():
    """
    更新仓库
    ---
    parameters:
      - name: id
        in: formData
        type: string
        required: true
      - name: name
        in: formData
        type: string
        required: false
      - name: description
        in: formData
        type: string
        required: false
    responses:
      200:
        description: 仓库
        schema:
          $ref: '#/definitions/Project'
    """
    return ProjectService(request.values).update_project()


@main.route('/projects/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    """
    删除仓库
    ---
    parameters:
      - name: id
        in: formData
        type: string
        required: true
    responses:
      200:
        description: 仓库
        schema:
          $ref: '#/definitions/Project'
    """
    return ProjectService(request.values).delete_project(project_id)


@main.route('/projects/<int:project_id>/auth', methods=['POST'])
def save_project_auth(project_id):
    """
    更新仓库权限
    ---
    parameters:
      - name: project_id
        in: path
        type: string
        required: true
      - name: setting_auth_content
        in: formData
        type: string
        required: true
    responses:
      200:
        description: 仓库
        schema:
          $ref: '#/definitions/Project'
    """
    setting_auth_content = request.values.get('setting_auth_content', type=str, default=None)
    if not project_id or not setting_auth_content:
        raise InvalidUsage(payload=ResponseEnum.INVALID_PARAMS)

    auth_list = setting_auth_content.replace(' ', '').split('\n')
    print(auth_list)
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
            if not re.search('^\\[[\\:|/|\\w]+\\]$', auth_line):
                err_msg = '第{0}行有错，[]未匹配'.format(index + 1)
                raise InvalidUsage(payload=(9000, err_msg))
            resouces.append(auth_line)
        elif resouces[-1] == '[groups]' and not auth_line.startswith('['):
            group, user_list = handle_group_line(index, auth_line)
            defined_groups.append(group)
            developers.append(user_list)
        else:
            if len(auth_line) == 0:
                continue
            group, user_list = handle_normal_line(index, auth_line)
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

    project.setting_auth_content = setting_auth_content
    project.save()

    return 'success'


def handle_group_line(index, auth_line):
    if not re.search('^\\w+=(\\w+,)*\\w+$', auth_line):
        err_msg = '第{0}行出错，出现非法字符'.format(index + 1)
        raise InvalidUsage(payload=(9000, err_msg))
    group = auth_line.split('=')[0]
    users = auth_line.split('=')[1]
    user_list = users.split(',')
    return group, user_list


def handle_normal_line(index, auth_line):
    if not re.search('^@?\\w+=(r|rw)?$', auth_line):
        err_msg = '第{0}行出错，出现非法字符或权限不符合（r = 只读 rw = 读写 空 = 无权限）'.format(index + 1)
        raise InvalidUsage(payload=(9000, err_msg))
    if auth_line.startswith('@'):
        group = auth_line.split('=')[0].replace('@', '')
        return group, None

    user = auth_line.split('=')[0]
    return None, user
