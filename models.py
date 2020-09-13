
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:2313@localhost/CharitySystem'

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'userDetails'
    id = db.Column(db.Integer, primary_key=True , autoincrement=True)
    fullname = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
