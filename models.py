from exts import db


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    account = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)
