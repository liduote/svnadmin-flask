from datetime import datetime

from sqlalchemy import and_

from app.model import Member
from app.extensions.db_ext import db


class MemberService:
    def save_project_member(self, project_id, user_id, creator_id, access_level):
        member = Member.query.filter(and_(
            Member.source_id == project_id,
            Member.user_id == user_id
        )).first()
        if not member:
            member = Member()
            member.created_by = creator_id
            member.created_on = datetime.now()
            member.type = 'ProjectMember'
            member.source_type = 'Project'
            member.source_id = project_id
            member.user_id = user_id
            member.updated_on = datetime.now()
            member.access_level = access_level
            member.save()
        elif member.access_level != access_level:
            member.access_level = access_level
            member.updated_on = datetime.now()
            member.save()

    def del_project_member(self, project_id, user_id):
        member = Member.query.filter(and_(
            Member.source_id == project_id,
            Member.user_id == user_id,
            Member.source_type == 'Project'
        )).first()
        if member:
            member.delete_self()

    def delall_project_member(self, project_id):
        Member.query.filter(and_(
            Member.source_id == project_id,
            Member.source_type == 'Project'
        )).delete()
        db.session.commit()

    def delall_user_member(self, user_id):
        Member.query.filter(and_(
            Member.user_id == user_id
        )).delete()
        db.session.commit()


