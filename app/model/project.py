from app.extensions import db, BaseModel


class Project(BaseModel):
    __tablename__ = 'projects'
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(100))
    path = db.Column(db.String(100))
    description = db.Column(db.String(600))
    namespace_id = db.Column(db.INTEGER)
    visibility = db.Column(db.String(20))
    final_auth_content = db.Column(db.String(1000))
    setting_auth_content = db.Column(db.String(1000))
    last_activity_on = db.Column(db.DATETIME)
