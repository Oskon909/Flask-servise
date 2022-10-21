import json

import click
from flask import Flask, render_template, request, Response, current_app, jsonify
from flask.cli import AppGroup
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from connect_postgres import get_table

# from models import Category

app = Flask(__name__)
# db = SQLAlchemy(app)


with app.app_context():
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:akul6999@localhost/flask'
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
def index():
    with app.app_context():
        db.create_all()
        art = Category(name='Hipperion')
        print(db)

        db.session.add(art)
        db.session.commit()
        db.create_all()
    return Response('Hello World!')


@app.route('/100')
def send_date():
    with app.app_context():
        category=get_table()
        list_json_object= []
        category_json = {}
        for i in category:

            category_json['id'] =  i[0]
            category_json['name'] = i[1]
            list_json_object.append(category_json)
    context={'category':list_json_object[0]}
    return render_template('index.html', **context)




@app.route('/sub')
def Subcategory():
    with app.app_context():
        db.create_all()
        rest=Category.query.all()

        cat=Category.query.filter(Category.id == 12).first()
        print(cat.name,'---')

        ddd=Advert.query.all()
        print(ddd)

        ggg=Category.query.all()
        print(ggg)


        # art = Subcategory(name='Bishkek')
        # print(db)
        #
        # db.session.add(art)
        # db.session.commit()
        # db.create_all()
    return Response('Hello World!')


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
    app.run(host='0.0.0.0', port=8001, debug=True)
