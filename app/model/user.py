from app.extensions import db, BaseModel, AlchemyEncoder


class User(BaseModel):
    __tablename__ = 'users'
    id = db.Column(db.INTEGER, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    fullname = db.Column(db.String(100))
    email = db.Column(db.String(100))
    sign_in_count = db.Column(db.Integer)
    project_limits = db.Column(db.Integer)
    state = db.Column(db.String(20))
    last_activity_on = db.Column(db.DATETIME)
    admin = db.Column(db.Integer)
