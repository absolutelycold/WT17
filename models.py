from exts import db


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    account = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text, nullable=False)
    is_admin = db.Column(db.Integer, default=0)


class Goods(db.Model):
    __tablename__ = 'goods'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    good_name = db.Column(db.String(50), nullable=False, default='No name')
    good_desc = db.Column(db.String(200), nullable=False, default='No description')
    picture_url = db.Column(db.String(200), nullable=True)
