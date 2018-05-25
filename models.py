from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

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
    good_price = db.Column(db.Integer, nullable=False, default=0)
    good_name = db.Column(db.String(50), nullable=False, default='No name')
    good_desc = db.Column(db.String(200), nullable=False, default='No description')
    picture_url = db.Column(db.String(200), nullable=True)
    class_id = db.Column(db.Integer)


class Goods_class(db.Model):
    __tablename__ = 'goods_class'
    class_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    class_name = db.Column(db.String(50), nullable=False)


class Cart(db.Model):
    __tablename__ = 'cart'
    cart_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    goods_id = db.Column(db.Integer, nullable=False)
    goods_num = db.Column(db.Integer, nullable=False)
