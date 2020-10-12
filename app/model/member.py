from app.extensions import db, BaseModel


class Member(BaseModel):
    __tablename__ = 'members'
    id = db.Column(db.INTEGER, primary_key=True)
    source_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    access_level = db.Column(db.Integer)
    source_type = db.Column(db.String(100))
    type = db.Column(db.String(100))
