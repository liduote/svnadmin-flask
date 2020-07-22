import json
from flask import request

from . import main
from app.service import ProjectService
from app.extensions import AlchemyEncoder


@main.route('/projects', methods=['GET'])
def get_project_list():
    """
    获取仓库列表
    ---
    tags:
      - 项目
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
    tags:
      - 项目
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
    tags:
      - 项目
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
    tags:
      - 项目
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
    tags:
      - 项目
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
    return ProjectService(request.values).delete_project(project_id)


@main.route('/projects/<int:project_id>/auth', methods=['POST'])
def update_project_auth(project_id):
    """
    更新仓库权限
    ---
    tags:
      - 项目
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
    return ProjectService(request.values).update_project_auth(project_id)
