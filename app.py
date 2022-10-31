import json

import click
from flask import Flask, render_template, request, Response, current_app, jsonify
from flask.cli import AppGroup
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

with app.app_context():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db:5432'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = '123456790'
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)


class Category(db.Model):
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


@app.route('/12')
@app.route('/login', methods=['POST', 'GET'])
def index():
    print(request.json)
    # request.data = json.loads(request.data)
    # print(request.data,'------------')
    # with app.app_context():


    return {'status': 'ok'}






with app.app_context():
    admin = Admin(app, name='microblog', template_mode='bootstrap3')
    admin.add_view(ModelView(Category, db.session))
    admin.add_view(ModelView(City, db.session))
    admin.add_view(ModelView(SubCategory, db.session))
    admin.add_view(ModelView(Advert, db.session))

with app.app_context():
    db.create_all()


@app.cli.command("create-user")
@click.argument("name")
def create_user(name):
    print(f"Creating user {name}...")
    # call your method here


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
