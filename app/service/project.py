from datetime import datetime

from sqlalchemy import or_

from app.enum import BusiEnum, ResponseEnum
from app.model.project import Project
from app.exception import InvalidUsage


class ProjectService:
    def __init__(self, values):
        self.id = values.get(key='id', type=int, default=None)
        self.name = values.get(key='name', type=str, default=None)
        self.path = values.get(key='path', type=str, default=None)
        self.description = values.get(key='description', type=str, default=None)
        self.visibility = values.get(key='visibility', type=str, default=None)
        self.initDirs = values.get(key='initDirs', type=bool, default=False)
        self.searchValue = values.get(key='searchValue', type=str, default=None)

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
        project = Project()
        project.name = self.name
        project.path = self.path
        project.description = self.description
        project.visibility = self.visibility
        project.setting_auth_content = self.generate_setting_auth_content()
        project.final_auth_content = self.generate_final_auth_content()
        project.last_activity_on = datetime.now()
        project.save()
        return project.to_json()

    def get_by_id(self, project_id):
        if not project_id:
            raise InvalidUsage(payload=ResponseEnum.INVALID_PARAMS)
        return Project.query.get(project_id).to_json()

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
        return project.to_json()

    def delete_project(self, project_id):
        if not project_id:
            raise InvalidUsage(payload=ResponseEnum.INVALID_PARAMS)
        project = Project.query.get(project_id)
        if not project:
            return 'success'
        project.delete_self()
        return 'success'

    def search(self):
        if self.searchValue:
            return Project.query.filter(or_(
                Project.name.like('%' + self.searchValue + '%'),
                Project.path.like('%' + self.searchValue + '%'),
                Project.description.like('%' + self.searchValue + '%')
            )).order_by(Project.last_activity_on.desc()).all()
        else:
            return Project.query.all()

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
