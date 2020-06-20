from app.extensions import db, BaseModel


class User(BaseModel):
    __tablename__ = 'users'
    id = db.Column(db.INTEGER, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
