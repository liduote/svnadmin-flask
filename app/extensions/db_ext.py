import json
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import DeclarativeMeta

db = SQLAlchemy()


class BaseModel(db.Model):
    __abstract__ = True
    created_on = db.Column(db.DATETIME, default=datetime.now)
    updated_on = db.Column(db.DATETIME, default=datetime.now)
    created_by = db.Column(db.INTEGER)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def delete(obj):
        db.session.delete(obj)
        db.session.commit()

    @staticmethod
    def update():
        db.session.commit()

    def delete_self(self):
        db.session.delete(self)
        db.session.commit()

    def to_json(self):
        return json.dumps(self, cls=AlchemyEncoder)

    def to_dict(self):
        return json.loads(self.to_json())


class AlchemyEncoder(json.JSONEncoder):
    """
    SqlAlchemy对象转换为json格式
    """
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            fields = {}
            for field in [x for x in dir(obj)]:
                if field.startswith('_'):
                    continue
                if field == 'metadata':
                    continue
                if callable(getattr(obj, field)):
                    continue
                if field == 'query':
                    continue
                data = obj.__getattribute__(field)
                try:
                    if type(data) is datetime:
                        data = data.strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        json.dumps(data)
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            return fields
        return json.JSONEncoder.default(self, obj)
