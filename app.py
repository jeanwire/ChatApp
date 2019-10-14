from flask import Flask
from flask_sqlalchemy import SQLAlchemy

 app = Flask(__name__)

 app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:G8AR7Cseu5bTh9pPttcX@localhost/flowgames'
 app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
 db = SQLAlchemy(app)

 class User(db.Model):
     __tablename__ = 'users'
     id = db.Column(db.Integer, primary_key=True, unique=True)
     username = db.Column(db.String(64), unique=True)
     password = db.Column(db.String(128))
     # how does backref work??
     messages_sent = db.relationship('Message', backref='sender_id')
     messages_received = db.relationship('Message', backref='receiver_id')


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    timestamp = db.Column(db.DateTime)
    sender = db.Column(db.Integer, db.ForeignKey('users.id'))
    receiver = db.Column(db.Integer, db.ForeignKey('users.id'))
