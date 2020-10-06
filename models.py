
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:2313@localhost/CharitySystem'

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'userDetails'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fullname = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    phone = db.Column(db.String,nullable=False)
    password = db.Column(db.String, nullable=False)


class Charity(db.Model):
    __tablename__ = 'charityDetails'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(120),default='image.jpg')
    pub_time = db.Column(db.Date, nullable=False,default=datetime.utcnow)

