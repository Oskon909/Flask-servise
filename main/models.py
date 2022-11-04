from flask_serialize import FlaskSerialize

from main.config import db


fs_mixin = FlaskSerialize(db)

class Category(db.Model, fs_mixin):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())


class SubCategory(db.Model):
    __tablename__ = 'subcategory'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    category = db.Column(db.Integer(), db.ForeignKey('category.id'))


class AdvertImage(db.Model):
    __tablename__ = 'advertimage'
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String())
    advert = db.Column(db.Integer(), db.ForeignKey('advert.id'))


class City(db.Model):
    __tablename__ = 'city'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())


class Advert(db.Model):
    __tablename__ = 'advert'
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.Integer(), nullable=True)
    name = db.Column(db.String(), nullable=True)
    description = db.Column(db.String())
    from_price = db.Column(db.Integer(), nullable=True)
    email = db.Column(db.String(), nullable=True)
    wa_number = db.Column(db.String(), nullable=True)
    status = db.Column(db.String(), nullable=True)
    category = db.Column(db.Integer(), db.ForeignKey('category.id'), nullable=True)
    subcategory = db.Column(db.Integer(), db.ForeignKey('subcategory.id'), nullable=True)
    city = db.Column(db.Integer(), db.ForeignKey('city.id'), nullable=True)

