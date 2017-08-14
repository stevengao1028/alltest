# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

basedir= os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///'+ os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] =True
db = SQLAlchemy(app)


class User(db.Model):
    """定义数据模型"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

@app.route('/')
def hello_world():
    # db.create_all()
    # admin = User('admin', 'admin@example.com')
    # guest = User('guest', 'guest@example.com')
    # db.session.add(admin)
    # db.session.add(guest)
    # db.session.commit()
    users = User.query.filter_by(username='guest').first()
    print users.username
    return users.username
if __name__ == '__main__':
    app.run(debug = True)


# -*- coding: utf-8 -*-

