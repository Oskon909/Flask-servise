from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from main.app import app

with app.app_context():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db:5432'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = '123456790'
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)


